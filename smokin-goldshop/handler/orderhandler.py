
import os, re, math, urllib, logging, datetime, random, unicodedata, json, uuid
from public import mechanize
from google.appengine.api import memcache, users, taskqueue, mail, urlfetch
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

from models.agent import Agent
from models.order import Order
from models.customer import Customer
from models.referrer import Referrer
from models.phone import Phone
from models.promo import Promo
from models.ipinfo import IpInfo

from handler.stockaccountmanager import StockAccountManager
from handler.customerhandler import CustomerHandler
from iplookup import IpLookup
from phonelookup import PhoneLookup
from verifyemail import VerifyEmail
from verifyphone import VerifyPhone
from referral import Referral, ReferralBalance

from stockmanager import StockManager
from stockaccountmanager import StockAccountManager
from models.stockaccount import StockAccount

from _data import PriceContainer, CountryContainer
from _numbertogp import NumberToGp
from base import BaseHandler

class OrderHandler(BaseHandler):
    #Modified for account security
    API_PASSWORD  = "REDACTED"
    API_USERNAME  = "REDACTED"
    API_SIGNATURE = "REDACTED"
    
    LOCATION = "../views/order.html"
    def GetContext(self):
        tUser = self.GetUser()
        
        tCustomerOrders = []
        tOrderData = {}
        tContext = {}
        
        tOrder = Order()
        tCustomer = Customer()
        tIpHandler = IpLookup()
        tIpInfo = IpInfo()
        
        tDeliveryAgent = Agent()
        tRefundAgent = Agent()
        tAssignedAgent = Agent()
        
        tPriceDic = PriceContainer.GetCurrentPriceDic()
        tCountryDic = CountryContainer.GetCurrentCountryCodes()
        tOrderKey = str(urllib.unquote(self.request.get('key')))
        
        if(tOrderKey != None and len(tOrderKey) > 0):
            tOrder = Order.get(tOrderKey)
        if(tOrder):
            tOrderHandler = OrderHandler()
            
            tResultDictionary = {}
            tPaypalPayload = {}        
            tPayload = {}
            
            tUrl = "https://api-3t.paypal.com/nvp"
            tOperation = "GetTransactionDetails"            
            tCustomer = Customer.get(tOrder.orderCustomer)
                        
            # disabled to try to trace the "empty order" bug
            #if tOrder.orderVerificationCode is None:
                #tOrder.orderVerificationCode = str(uuid.uuid4())
                #tOrder.put()                    
            
            try:
                tIpInfo = tIpHandler.GetIp(tOrder.orderIp)[0]
            except:
                tIpInfo.ipCountry = "Loading"
                tIpInfo.ipState = "Loading"
                tIpInfo.ipHost = "Loading"
                tIpInfo.ipProxy = "Loading"
                tIpInfo.ipIsp = "Loading"
                tIpInfo.ipType = "Loading"
            
            if (tIpInfo.ipProxy == ""):
                tIpInfo.ipProxy = 'No Proxy'
            tContext['tDisplayDeliver'] = 'True'
                        
            #Get Paypal Information
            tPaypalPayload['METHOD'] = tOperation
            tPaypalPayload['TRANSACTIONID'] = tOrder.orderTransactionId
            
            #logging.debug("Order Paypal Email: " + tOrder.orderPaypalEmail)
            
            try:
                tPayloadEncoded = tOrderHandler.GeneratePayload(tPaypalPayload)
                request_cookies = mechanize.CookieJar()
                request_opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(request_cookies))
                request_opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
                mechanize.install_opener(request_opener)
                tResponse = mechanize.urlopen(url = tUrl, timeout = 25.0, data = tPayloadEncoded)
            except: 
                tContext['error'] = 'Unable to Connect to Paypal, Try Refreshing'
                tContext['showerror'] = 'True'
                #tmpl = os.path.join(os.path.dirname(__file__), '../views/order.html')
                #self.response.out.write(render(tmpl, tContext))
                return tContext
                
            tResult = str(urllib.unquote(tResponse.read()))
            tResultSplit = tResult.split('&')
            
            for tPair in tResultSplit:
                tSplitPair = tPair.split("=")
                try:
                    tResultDictionary[tSplitPair[0]] = tSplitPair[1]
                    #logging.debug(tSplitPair[0] + "    " + tSplitPair[1])
                except:
                    logging.error("Error splitting item: " + str(tPair))
            
            if('COUNTRYCODE' in tResultDictionary.keys()):
                tCountryCode = tResultDictionary['COUNTRYCODE']
                tPaypalCountry = tCountryDic[tCountryCode]
            else:
                tPaypalCountry = 'UNKNOWN'
                
            tOrderData['paypalcountry'] = tPaypalCountry                    
            
            if 'PROTECTIONELIGIBILITYTYPE' in tResultDictionary.keys():
                tProtectionEligibility = tResultDictionary['PROTECTIONELIGIBILITYTYPE']
                
                if tProtectionEligibility == 'ItemNotReceivedEligible,UnauthorizedPaymentEligible':
                    tProtectionEligibility = 'Eligible'
                    
                if tProtectionEligibility != 'Eligible':
                    tProtectionEligibility = 'Not Eligible'
                    
                tContext['PROTECTIONELIGIBILITYTYPE'] = tProtectionEligibility
            else:
                tProtectionEligibility = 'UNKNOWN'
                
            #Display address fields
            if 'ADDRESSSTATUS' in tResultDictionary.keys():
                tContext['ADDRESSSTATUS'] = tResultDictionary['ADDRESSSTATUS']
            else:
                tContext['ADDRESSSTATUS'] = 'UNKNOWN'
            
            if 'SHIPTONAME' in tResultDictionary.keys():
                tContext['SHIPTONAME'] = tResultDictionary['SHIPTONAME']
            else:
                tContext['SHIPTONAME'] = 'UNKNOWN'
                
            if 'SHIPTOSTREET' in tResultDictionary.keys():
                tContext['SHIPTOSTREET'] = tResultDictionary['SHIPTOSTREET']
            else:
                tContext['SHIPTOSTREET'] = 'UNKNOWN'
                
            if 'SHIPTOSTREET2' in tResultDictionary.keys():
                tContext['SHIPTOSTREET2'] = tResultDictionary['SHIPTOSTREET2']
            else:
                tContext['SHIPTOSTREET2'] = 'UNKNOWN'
                
            if 'SHIPTOCITY' in tResultDictionary.keys():
                tContext['SHIPTOCITY'] = tResultDictionary['SHIPTOCITY']
            else:
                tContext['SHIPTOCITY'] = 'UNKNOWN'
                
            if 'SHIPTOSTATE' in tResultDictionary.keys():
                tContext['SHIPTOSTATE'] = tResultDictionary['SHIPTOSTATE']
            else:
                tContext['SHIPTOSTATE'] = 'UNKNOWN'
                            
            if 'SHIPTOZIP' in tResultDictionary.keys():
                tContext['SHIPTOZIP'] = tResultDictionary['SHIPTOZIP']
            else:
                tContext['SHIPTOZIP'] = 'UNKNOWN'
                
            if 'SHIPTOCOUNTRYCODE' in tResultDictionary.keys():
                tContext['SHIPTOCOUNTRYCODE'] = tResultDictionary['SHIPTOCOUNTRYCODE']
            else:
                tContext['SHIPTOCOUNTRYCODE'] = 'UNKNOWN'
                
            if 'SHIPTOPHONENUM' in tResultDictionary.keys():
                tContext['SHIPTOPHONENUM'] = tResultDictionary['SHIPTOPHONENUM']
            else:
                tContext['SHIPTOPHONENUM'] = 'UNKNOWN'
                
            
            #Get order amount to add to dated totals
            tCurrentCost = float(tOrder.orderCost)
            
            #Get date 30 days ago
            tStartDate = tOrder.orderCreated
            tIncrement = datetime.timedelta(days = -30)
            tEndDate = tStartDate + tIncrement
            tCustomerOrderQuery = Order.all()
            tCustomerOrderQuery.filter("orderCreated >", tEndDate)
            tCustomerOrderQuery.filter("orderCustomer", tOrder.orderCustomer)
            tCustomerOrderQuery.filter("orderDeliver", 'True')
            tCustomerOrders = tCustomerOrderQuery.fetch(1000)
            #logging.debug("30 day date: " + str(tEndDate))
            #logging.debug("30 day orders: " + str(len(tCustomerOrders)))
            tCustomerOrderTotal = 0.0
            for tCustomerOrder in tCustomerOrders:
                tCustomerOrderTotal += float(tCustomerOrder.orderCost)
            if (tOrder.orderDeliver == 'False'):
                tCustomerOrderTotal += tCurrentCost
            tOrderData['orderTotal'] = str("%.2f"% tCustomerOrderTotal)
            
            #Get date 24 hours ago
            tStartDate = tOrder.orderCreated
            tIncrement = datetime.timedelta(days = -1)
            tEndDate = tStartDate + tIncrement
            tCustomerOrderQuery = Order.all().filter("orderCreated >", tEndDate)
            tCustomerOrderQuery.filter("orderCustomer", tOrder.orderCustomer)
            tCustomerOrderQuery.filter("orderDeliver", 'True')
            tCustomerOrders = tCustomerOrderQuery.fetch(1000)
            #logging.debug("24 hour date: " + str(tEndDate))
            #logging.debug("24 hour orders: " + str(len(tCustomerOrders)))
            tCustomerOrderTotal24 = 0.0
            for tCustomerOrder in tCustomerOrders:
                tCustomerOrderTotal24 += float(tCustomerOrder.orderCost)
                
            if (tOrder.orderDeliver == 'False'):
                tCustomerOrderTotal24 += tCurrentCost
            tOrderData['orderTotal24'] = str("%.2f" % tCustomerOrderTotal24)
            
            #Get date 15 days ago
            tStartDate = tOrder.orderCreated
            tIncrement = datetime.timedelta(days = -15)
            tEndDate = tStartDate + tIncrement
            tCustomerOrderQuery = Order.all().filter("orderCreated >", tEndDate)
            tCustomerOrderQuery.filter("orderCustomer", tOrder.orderCustomer)
            tCustomerOrderQuery.filter("orderDeliver", 'True')
            tCustomerOrders = tCustomerOrderQuery.fetch(1000)
            #logging.debug("15 day date: " + str(tEndDate))
            #logging.debug("15 day orders: " + str(len(tCustomerOrders)))
            tCustomerOrderTotal15 = 0.0
            for tCustomerOrder in tCustomerOrders:
                tCustomerOrderTotal15 += float(tCustomerOrder.orderCost)
                
            if (tOrder.orderDeliver == 'False'):
                tCustomerOrderTotal15 += tCurrentCost
            tOrderData['orderTotal15'] = str("%.2f" % tCustomerOrderTotal15)
            
            #===== Begin Location Matching =====
            try:
                tPhoneHandler = PhoneLookup()
                tPhoneInfo = tPhoneHandler.GetPhone(tOrder.orderCustomer)[0]
            except:
                tPhoneInfo = Phone()
                tPhoneInfo.phoneState = "Unknown"
                tPhoneInfo.phoneCountry = "Unknown"
            
            #logging.debug("Ip country: " + str(tIpInfo.ipCountry))
            #logging.debug("Paypal country: " + str(tPaypalCountry))
            
            if (str(tIpInfo.ipCountry) == str(tPaypalCountry)):
                tOrderData['locationmatch'] = 'True'
            else:
                tOrderData['locationmatch'] = 'False'
                
            if (str(tIpInfo.ipCountry) == "United Kingdom" and str(tPaypalCountry) == "Great Britain (UK)"):
                tOrderData['locationmatch'] = 'True'
                
            #Agent Instructions
            #logging.debug("Order Total 24: " + str(tCustomerOrderTotal24))
            #logging.debug("Order Total: " + str(tCustomerOrderTotal))
            #logging.debug("Customer email verified: " + str(tCustomer.customerEmailVerified))
            #logging.debug("Customer phone verified: " + str(tCustomer.customerPhoneVerified))
            #logging.debug("Customer id verified: " + str(tCustomer.customerIdVerified))
            
            #Protection Eligibility Filter 
            tCountryEligibilityCode = tContext['SHIPTOCOUNTRYCODE']
            tOrderData['instructions'] = "No verification required" # default value
            if tCountryEligibilityCode in ('US', 'UK', 'CA', 'GB'):  
                if tOrder.orderCost > 10:              
                    if tProtectionEligibility == 'Eligible':
                        if tCustomerOrderTotal24 > 1000.0 or tCustomerOrderTotal > 4000.0:
                            tOrderData['instructions'] = "<span style='color:red'>$$$ Call Corowns $$$</span>"   
                    else: # not payment eligible
                        tOrderData['instructions'] = "<span style='color:red'>Refund - No Seller Protection</span>"
                        tContext['tDisplayDeliver'] = 'False'
            else: # international customer
                #if( tCustomerOrderTotal24 < 30.0 and tCustomerOrderTotal < 60.0):
                
                if tIpInfo.ipType == "Corporate":
                    tOrderData['instructions'] = tOrderData['instructions'] + "<br /><span style='color:red'>Refer to PA - Corporate IP</span>"
                    tOrderData['tDisplayDeliver'] = 'False'
                    
                if (tIpInfo.ipProxy):
                    if ("Confirmed proxy server" == tIpInfo.ipProxy):
                        tOrderData['instructions'] = tOrderData['instructions'] + "<br /><span style='color:red'>Refer to PA - Proxy</span>"
                        tContext['tDisplaydeliver'] = 'False'
                
                if tCustomerOrderTotal24 > 200.0 or tCustomerOrderTotal > 400.0:
                    tOrderData['instructions'] = "<span style='color:red'>Refer to PA - Limit Exceeded</span>"
                    tOrderData['tDisplayDeliver'] = 'False'                   
                elif tCustomerOrderTotal24 > 90.0 or tCustomerOrderTotal > 180.0:
                    if tCustomer.customerIdVerified != True:
                        tOrderData['instructions'] = "<span style='color:red'>Verify Photo ID</span>"        
                elif tCustomerOrderTotal24 > 30.0 or tCustomerOrderTotal > 60.0:
                    if tCustomer.customerPhoneVerified != True:
                        tOrderData['instructions'] = "<span style='color:red'>Verify Phone Number</span>"
                
            if(tOrderData['locationmatch'] != 'True'):
                tOrderData['instructions'] = tOrderData['instructions'] + "<br /><span style='color:red'>Verify Country Match</span>"
                                
            #logging.debug("Order Data Instructions: " + str(tOrderData['instructions']))
            #logging.debug("Location Match" + str(tOrderData['locationmatch']))
            
            tCustomerOrderQuery = db.GqlQuery("SELECT * FROM Order WHERE orderCustomer = '" + tOrder.orderCustomer + "'")
            tTotalCustomerOrders = []
            tTotalCustomerOrders = tCustomerOrderQuery.fetch(50)
            for tCustomerOrder in tTotalCustomerOrders:
                if (tCustomerOrder.orderChargeback == True):
                    tChargeBack = True
                else:
                    tChargeBack = False
                    
            tOrderData['chargeback'] = tChargeBack if (tChargeBack) else False
            tOrderData['chargeback'] = str(tOrderData['chargeback'])
            
            tIpChargebacks = tIpHandler.GetChargebacks(tOrder.orderIp)
            tOrderData['ipchargeback'] = len(tIpChargebacks)
                            
            try:
                tTotalBonusString = NumberToGp.ConvertIntToBet(int(tOrder.orderBonusQuantity))
                #logging.debug("Total Bonus String " + tTotalBonusString)
            except:
                tTotalBonusString = ""
                
            if (tCustomer.customerIsPaBlacklisted == True):
                tOrderData['instructions'] = tOrderData['instructions'] + "<br /><span style='color:red'>Refer to PA - Blacklist</span>"
                tContext['tDisplayDeliver'] = 'False'
                
            if (tCustomer.customerIsGlobalBlacklisted == True):
                tOrderData['instructions'] = tOrderData['instructions'] + "<br /><span style='color:red'>Do Not Deliver - Blacklist</span>"
                tContext['tDisplayDeliver'] = 'False'
            
            #normalize unicode
            try:
                tSimpleGold = unicodedata.normalize("NFC", tOrder.orderSimpleGoldAmount).encode("ascii", "ignore")
            except:
                tSimpleGold = tOrder.orderSimpleGoldAmount
            
            #logging.debug(str(tPriceDic[tSimpleGold]))
            #logging.debug(str(tOrder.orderCost))
            tCurrentEocPrices = PriceContainer.GetCurrentPriceDic()
            tCurrent07Prices = PriceContainer.GetCurrentPriceDic07()
                        
            #logging.debug(str(tCurrent07Prices))
            #logging.debug(str(tCurrentEocPrices))
            
            tSkip07 = False
            tValidOrder = False
            if tOrder.orderSimpleGoldAmount in tCurrentEocPrices.keys():
                if str(tOrder.orderCost) == str(tCurrentEocPrices[tOrder.orderSimpleGoldAmount]):
                    tOrder.orderGoldType = 'eoc'
                    tSkip07 = True
                    tValidOrder = True
            
            if not tSkip07:
                if tOrder.orderSimpleGoldAmount in tCurrent07Prices.keys():
                    if str(tOrder.orderCost) == str(tCurrent07Prices[tOrder.orderSimpleGoldAmount]):
                        tOrder.orderGoldType = '07'
                        tValidOrder = True
            
            #logging.debug("skip07 {}".format(tSkip07))
            #logging.debug("valid {}".format(tValidOrder))
            #logging.debug("order simple gold amount {}".format(tOrder.orderSimpleGoldAmount))
            #logging.debug("order value {}".format(tOrderData['orderTotal']))
            #logging.debug("gold type {}".format(tContext['gold_type']))
                        
            if not tValidOrder:
                tOrderData['instructions'] = tOrderData['instructions'] + '<br /><span style="color:red">Do Not Deliver - Bad Payment</span>'
                #tOrderData['tDisplayDeliver'] = 'False'
                #tOrder.orderLocked = 'True'
                #tOrder.put()
            
            #logging.debug(str(tOrder.orderIsGenerated))
            if(tOrder.orderIsGenerated == True):
                tOrder.orderLocked = 'False'
                tOrder.orderIsRefunded = 'False'
                tOrder.orderDeliver = 'False'
                tOrderData['tDisplayDeliver'] = 'True'
                
            try:
                tDeliveryAgent = Agent.GetAgentByEmail(tOrder.orderDeliveryAgent)
                tContext['tDeliveryAgent'] = tDeliveryAgent
            except:
                pass
            
            try:
                tAssignedAgent = Agent.GetAgentByEmail(tOrder.orderAssignedAgent)
                tContext['tAssignedAgent'] = tAssignedAgent
            except:
                pass
            
            try:
                tRefundAgent = Agent.GetAgentByEmail(tOrder.orderRefundAgent)
                tContext['tRefundAgent'] = tRefundAgent
            except:
                pass            
            tOrderData['bonus'] = tTotalBonusString
            
            tOrderData['phoneverified'] = str(tCustomer.customerPhoneVerified)
            tOrderData['emailverified'] = str(tCustomer.customerEmailVerified)
            tOrderData['idverified'] = str(tCustomer.customerIdVerified)
            
            tContext['tOrder'] = tOrder
            tContext['tOrderData'] = tOrderData
            tContext['tCustomer'] = tCustomer
            tContext['tIpInfo'] = tIpInfo
            tContext['tPhoneInfo'] = tPhoneInfo
        
        
        if ((tOrder.orderDeliveryAgent == "" or tOrder.orderDeliveryAgent == None) and tOrder.orderDeliver == 'True'):
            tAgentKey = tOrder.orderAgent
            tAgentId = Agent()
            tAgentId = Agent.get(tAgentKey)
            tOrder.orderDeliveryAgent = str(tAgentId.agentId)
                        
        #logging.debug(str(tOrderData))
        return tContext
            
    def GeneratePayload(self, pPayload):
        tPayload = {}
        tPayload = pPayload
        tBasePayload = {
            "USER" : self.API_USERNAME,
            "PWD" : self.API_PASSWORD,
            "SIGNATURE" : self.API_SIGNATURE,
            "VERSION" : "72.0"
            }
        
        for tKey in tPayload.keys():
            tBasePayload[tKey] = tPayload[tKey]
        
        return urllib.urlencode(tBasePayload)
            

class OrderLookup(webapp.RequestHandler):
    LOCATION = "../views/order.html"
    def GetContext(self):
        tContext = {}
        tOrderKey = str(urllib.unquote(self.request.get('key')))
        if(tOrderKey != None and len(tOrderKey) > 0):
            tOrder = Order.get(tOrderKey)
            tContext['tOrder'] = tOrder            
                
        return tContext
            
class DeliverOrder(webapp.RequestHandler):
    def post(self):
        tOrderKey = self.request.get('orderid')
        tAgentGold = self.request.get('agentgold')
        
        #logging.debug("tOrderKey: " + tOrderKey)
        #logging.debug("tAgentGold: " + tAgentGold)
        tOrder = Order()
        tOrder = Order.get(tOrderKey)
        tUser = users.get_current_user()
        tAgent = Agent().GetAgentByEmail(str(tUser.email()))
        
        if (tOrder.orderDeliver == "" or tOrder.orderDeliver == 'False' and tOrder.orderLocked != 'True' and tAgent.agentIsEnabled == True):
                
            tGoldAmount = tOrder.orderQuantity
            tPromoCode = ""
            tPromoCode = tOrder.orderPromotionalCode
            tPromo = Promo()
            tPromoCode = tPromoCode.lower()
            tReferCode = tOrder.orderReferralCode
            tCustomerLookup = CustomerHandler()
            tCustomer = Customer()
            
            tCustomer = Customer().get(str(tOrder.orderCustomer))
            # Promo codes get unlimited uses per customer
            # tUsedBonus = Order.GetCustomerPromoCodes(tCustomer.customerPaypalId)
            # tUsedBonus = tCustomer.customerUsedBonus
            # logging.debug("Customer used bonuses: " + str(tUsedBonus))
            # logging.debug("Order Promo Code: " + str(tPromoCode))
            tUsedBonus = [] 
            
            try:
                tPromo = Promo.GetPromoByCode(tPromoCode)
                # logging.debug(str(tPromo.promoGoldAmount))
                # logging.debug(str(tPromo.promoPercentage))
                # logging.debug(str(tPromo.promoIsActive))
                
                if ((tPromo.promoIsActive) and (tPromo.promoUses <= tPromo.promoLimit)):
                    if (tPromo.promoLimit != 0):
                        tPromo.promoUses = tPromo.promoUses + 1
                    
                    if((tPromoCode in tUsedBonus) == True):
                        tPercentBonus = 0.0
                    else:
                        tPercentBonus = float(tGoldAmount) * tPromo.promoPercentage
                        #tUsedBonus.append(tPromoCode)
                        
                    tGoldAmount = tGoldAmount + tPercentBonus
                    tGoldAmount = tGoldAmount + tPromo.promoGoldAmount
                    tTotalBonusFloat = tPercentBonus + tPromo.promoGoldAmount
                    tOrder.orderBonusQuantity = int(tTotalBonusFloat)     
            except:
                tOrder.orderBonusQuantity = 0
                
            tGoldAmountLong = tGoldAmount
            tGoldAmount = tGoldAmount / 1000000
            
            tOrderValue = float(tOrder.orderCost)
            
            #if(tOrder.orderIsGenerated == True):
                #tGoldAmountLong = 0
                #tGoldAmount = 0
            
                
            tStockManager = StockManager()
            tStockManager.LoadAccounts()            
            tStockManager.PlaceOrder(tGoldAmountLong * -1, tOrder.orderGoldType)            
                            
            #if tOrder.orderGoldType == '07':
                #tStockAccountManager.Set07Stock(int(tGoldAmountLong * -1))
            #else:
                #tStockAccountManager.SetEOCStock(int(tGoldAmountLong * -1))
                            
            tCommission = float(tOrderValue) * 0.05 + 0.50
            
            if tCommission >= 10.0:
                tCommission = 10.0                           
                
            tAgent.agentCurrentCommission = float(tAgent.agentCurrentCommission + tCommission)
            tAgent.agentTotalCommission = float(tAgent.agentTotalCommission + tCommission)                
            
            tAgentOrders = tAgent.agentOrders
            tAgentOrders.append(tOrderKey)
            tAgent.agentOrders = tAgentOrders
            tAgentKey = tAgent.put()
            tOrder.orderDeliveryAgent = str(tAgent.agentId)
            tOrder.orderAgent = str(tAgentKey)
            tOrder.orderDeliver = 'True'
            tKey = tOrder.put()
            
            #logging.debug("Delivery by Agent: " + str(tAgentKey))
            #logging.debug("Delivery of Order: " + str(tKey))
            
            #taskqueue.add(url='/calcreferral', countdown = 1, params={'key' : str(tKey) } )
            
            self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
            self.response.headers['Content-Type'] = 'Content-Type: plain/text'
            self.response.out.write("Order Delivered")
        else:
            #logging.debug('Attempted to Deliver ' + tOrderKey + " by Agent " + tAgent.agentId)
            self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
            self.response.headers['Content-Type'] = 'Content-Type: plain/text'
            self.response.out.write("Order Not Deliverable")