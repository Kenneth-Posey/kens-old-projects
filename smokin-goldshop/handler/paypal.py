
import os, re, math, urllib, logging, datetime, time, webapp2, uuid
from public import mechanize    
from random import choice
from google.appengine.api import memcache, users, urlfetch, taskqueue, mail
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import Request, RequestHandler
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

from paypalrefund import PaypalRefund
from orderhandler import OrderHandler

from cStringIO import StringIO

from models.order import Order
from models.currenttimestamp import CurrentTimestamp
from models.customer import Customer
from models.agent import Agent
from models.paypalipn import PaypalIPN
from models.paorder import PaOrder
from models.vipsubscriber import VipSubscriber
from models.vipsubscription import VipSubscription
from models.vippayment import VipPayment

from _data import PriceContainer
from _stringmethods import StringMethods
from _numbertogp import NumberToGp
from customerhandler import CustomerHandler
from models.promo import Promo
from base import BaseHandler

class PaypalHandler(BaseHandler):
    LOCATION = "../views/paypal.html"
    def GetContext(self):
        tOrder = Order()
        tOrderList = []
        tOrderAgentPairs = {}
        tOrderDataDict = {}
        tPaypalOrder = PaypalOrder()
        tStringOffset = self.request.get('offset')
        if (len(tStringOffset) > 0):
            tOffset = int(tStringOffset)
        else:
            tOffset = 0
        
        tOrderQuery = Order.all()
        tOrderQuery.filter("orderIsGenerated", False)
        tOrderQuery.order('-orderCreated')
        tOrderList = tOrderQuery.fetch(10, offset = tOffset)
        
        tCurrentEocPrices = PriceContainer.GetCurrentPriceDic()
        tCurrent07Prices = PriceContainer.GetCurrentPriceDic07()
        
        tSkip07 = False
        
        if tOrder.orderGoldType != None:
            if tOrder.orderGoldType in ('eoc', '07') is not True:
                tOrder.orderGoldType = 'UNKNOWN'
        else:
            tOrder.orderGoldType = 'UNKNOWN'   
        
        for tOrder in tOrderList:                        
            
            if tOrder.orderSimpleGoldAmount in tCurrentEocPrices.keys():
                if str(tOrder.orderCost) == str(tCurrentEocPrices[tOrder.orderSimpleGoldAmount]):
                    tOrder.orderGoldType = 'eoc'
                    tSkip07 = True
            
            if not tSkip07:
                if tOrder.orderSimpleGoldAmount in tCurrent07Prices.keys():
                    if str(tOrder.orderCost) == str(tCurrent07Prices[tOrder.orderSimpleGoldAmount]):
                        tOrder.orderGoldType = '07' 
            #tOrder.orderSimpleGoldAmount = tOrder.orderSimpleGoldAmount + ' ' + str(tOrder.orderGoldType)
                        
            tOrderAgentPairs[str(tOrder.orderAssignedAgent)] = Agent.GetAgentByEmail(tOrder.orderAssignedAgent).agentNickName
            
        if (tOffset == 0):
            tPrev = tOffset
        else: 
            tPrev = tOffset - 10
        tOffset = tOffset + 10
        tNext = tOffset
        
        tOffset = str(tOffset)
        tNext = str(tNext)
        tPrev = str(tPrev)
        
        tAgent = tPaypalOrder.GetAssignedAgent()
        
        if(tAgent != "No Agent Online"):
            tAgent = Agent.GetAgentByEmail(tAgent).agentNickName
        
        tContext = {
            'orders':    tOrderList,
            'agents':    tOrderAgentPairs,
            'next':      tNext,
            'prev':      tPrev,
            'offset':    tOffset,
            'agent':     tAgent,
        }
        return tContext

    
class PaypalOrder(webapp2.RequestHandler):
    #Modified for account security
    API_PASSWORD  = "REDACTED"
    API_USERNAME  = "REDACTED"
    API_SIGNATURE = "REDACTED"
    def post(self):
        tCustomerHandler = CustomerHandler()
        tCustomer = Customer()
        tPaypalOrder = PaypalOrder()
        tIpnLogger = PaypalIPN()
        
        tCustomerList = []
        tIpList = []
        tOrderList = []
        
        tResultDictionary = {}
        tPaypalPayload = {}        
        tPayload = {}
        tArgumentDic = {}
        
        tRequest = self.request
        tArguments = tRequest.arguments()
        
        if (str(tRequest) == "VERIFIED"):
            return 
        
        for tArgument in tArguments:
            tArgumentDic[tArgument] = tRequest.get(tArgument)
            
            #For clearing placeholder data from goldshop form
            if (tArgumentDic[tArgument] == "."):
                tArgumentDic[tArgument] = ""
            
                
        #logging.debug("==========Beginning Request==========")
        
        tIpnLogger.ipnRawMessage = str(self.request)
        tIpnLogger._dynamic_properties = tArgumentDic
        tIpnLogger.put()
        
        for tArgKey in tArgumentDic.keys():            
            try:
                logging.debug("Paypal Post Key: " + str(tArgKey) + " with Value: " + str(tArgumentDic[tArgKey]))
            except:
                logging.debug("Error Storing Key: " + str(tArgKey))
            
        #logging.debug("==========Stored Request==========")
        if ((tArgumentDic.has_key('txn_type')) and (tArgumentDic['txn_type'] == "web_accept")):
            self.response.out.write("cmd=_notify-validate" + str(tRequest))
            if ((tArgumentDic.has_key('payment_status')) and (tArgumentDic['payment_status'] == "Completed")):
                tPaypalOrder.ProcessOrder(tArgumentDic)
            else:
                logging.debug("Attemped Storage Canceled Due To It Not Being Completed Status")
        
        if((tArgumentDic.has_key('case_type') and (len(tArgumentDic['case_type']) > 0))):
            tPaypalOrder.ProcessChargeback(tArgumentDic)
        elif(tArgumentDic.has_key('txn_type')):
            if(tArgumentDic['txn_type'] == "new_case"):
                tPaypalOrder.ProcessChargeback(tArgumentDic)
            #unsure why I included subscr_signup here
            #elif(tArgumentDic['txn_type'] == "subscr_payment" or tArgumentDic['txn_type'] == "subscr_signup"):
            elif (tArgumentDic['txn_type'] == "subscr_payment"):
                if(tArgumentDic.has_key('payment_status')):
                    if(tArgumentDic['payment_status'] == 'Completed'):
                        tPaypalOrder.ProcessSubscription(tArgumentDic)
                    else:
                        pass
            elif(tArgumentDic['txn_type'] == "subscr_cancel" or tArgumentDic['txn_type'] == "subscr_failed" or tArgumentDic['txn_type'] == "subscr_eot"):
                tPaypalOrder.ProcessSubscriptionCancellation(tArgumentDic)
        #elif((tArgumentDic.has_key('profile_status')) and (tArgumentDic['profile_status'] == "Suspended")):
            #tPaypalOrder.ProcessSubscriptionCancellation(tArgumentDic)
        elif((tArgumentDic.has_key('payment_status')) and (tArgumentDic['payment_status'] == "Reversed")):
            tPaypalOrder.ProcessChargeback(tArgumentDic)
                
    
    def ProcessOrder(self, pArgumentDic):
        tOrderHandler = OrderHandler()
        tCustomerHandler = CustomerHandler()
        tCustomer = Customer()
        tPaypalOrder = PaypalOrder()
        tArgumentDic = pArgumentDic
        
        #Assign Values from POST from Paypal IPN
        tTransactionId = tArgumentDic['txn_id']
        tAlphaMatch = re.compile('[^A-Za-z0-9]+')
        tAlphaSpaceMatch = re.compile('[^A-Za-z0-9 ]+')
        
        #Short circuits the order process for special PA page
        if('payer_email' in tArgumentDic.keys()):
            if(tArgumentDic['payer_email'] == 'paypal@playerauctions.com'):
                tPaypalOrder.ProcessPlayerAuctions(tArgumentDic)
                return    
            
        try:
            tGoldAmount = tArgumentDic['option_name7']
        except:
            tGoldAmount = ""
        
        try:
            tCustomerFirstName = tAlphaSpaceMatch.sub('', tArgumentDic['first_name'])
        except:
            tCustomerFirstName = ""
            
        try:
            tCustomerLastName = tAlphaSpaceMatch.sub('', tArgumentDic['last_name'])
        except:
            tCustomerLastName = ""
            
        try:
            tCustomerName = tAlphaSpaceMatch.sub('', tArgumentDic['option_name1'])
        except:
            tCustomerName = ""
        
        try:
            tEmail = tArgumentDic['option_name2']
        except:
            tEmail = ""
        tPaypalEmail = str(tArgumentDic['payer_email']).lower()
        try:
            tMobilePhone = tArgumentDic['option_name3']
            tMobilePhone = re.sub(r'\D', '', tMobilePhone)
        except:
            tMobilePhone = ""
        try:
            tRsName = tArgumentDic['option_name4'].strip().lower()
            tRsName = tRsName.replace(' ', '_')
            tRsName = tRsName.replace('-', '_')
        except:
            tRsName = ""
        try:
            tCombatLevel = ""
        except:
            tCombatLevel = ""
            
        #try:
            #tReferCode = str(tArgumentDic['option_name5']).strip()
        #except:
        tReferCode = ""
            
        try:
            tPromotionCode = str(tArgumentDic['option_name5']).strip()
        except:
            tPromotionCode = ""
        
        tOrderIp = tArgumentDic['custom']
        tMembers = ""

        try:
            tOrderQuery = Order.all().filter('orderTransactionId', tTransactionId)
            tOrder = tOrderQuery.fetch(1)[0]
        except: 
            tOrder = Order()
            
        if('fake' in tArgumentDic.keys()):
            #logging.debug('Fake key hit')
            #logging.debug(str(tArgumentDic['fake']))
            if (tArgumentDic['fake'] == 'True'):
                tOrder.orderIsGenerated = True
        
        tOrder.orderFormName = tCustomerName
        tOrder.orderCombatLevel = tCombatLevel
        
        if (len(tGoldAmount) == 0):
            tUrl = "https://api-3t.paypal.com/nvp"
            #tOperation = "AddressVerify"
            tOperation = "GetTransactionDetails"
            #Get Paypal Information
            #tPaypal = PaypalTrigger()
            tResultDictionary = {}
            tPaypalPayload = {}        
            tPayload = {}
            tPaypalPayload['METHOD'] = tOperation
            tPaypalPayload['TRANSACTIONID'] = tTransactionId
            
            tPayloadEncoded = tOrderHandler.GeneratePayload(tPaypalPayload)
            request_cookies = mechanize.CookieJar()
            request_opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(request_cookies))
            request_opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
            mechanize.install_opener(request_opener)
            tResponse = mechanize.urlopen(url = tUrl, timeout = 25.0, data = tPayloadEncoded)
            tResult = str(urllib.unquote(tResponse.read()))
            tResultSplit = tResult.split('&')
            
            for tPair in tResultSplit:
                tSplitPair = tPair.split("=")
                if(len(tSplitPair) == 1):
                    tSplitPair.append("")
                tResultDictionary[tSplitPair[0]] = tSplitPair[1]
                logging.debug(tSplitPair[0] + "    " + tSplitPair[1])
            tGoldAmountString = tResultDictionary['L_NAME0']
            logging.debug("Gold amount string %s".format(tGoldAmountString))
            try:
                tGoldRegex = re.compile("([0-9]*?[m|M]).T")
                tGoldMatch = tGoldRegex.findall(tGoldAmountString)
                #logging.debug("Backup gold amount parser hit, string " + tGoldAmountString + "   Match: " + tGoldMatch[0])
                tGoldAmount = tGoldMatch[0]
            except:
                tGoldRegex = re.compile("([0-9]*?[m|M]).T")
                tGoldMatch = tGoldRegex.findall(tGoldAmountString)
                try:
                    #logging.debug("Backup gold amount parser hit, string " + tGoldAmountString + "   Match: " + tGoldMatch[0])
                    tGoldAmount = tGoldMatch[0]
                except:
                    #logging.debug("No gold match")
                    tGoldAmount = ""
        
        tOrder.orderQuantity = NumberToGp.ConvertBetToInt(tGoldAmount)
        tOrder.orderSimpleGoldAmount = tGoldAmount
        tOrder.orderFormEmail = tEmail
        tOrder.orderAccountName = tRsName
        tOrder.orderMobileNumber = tMobilePhone
        tOrder.orderPromotionalCode = tPromotionCode.lower()
        tOrder.orderIp = tOrderIp
        if (tMembers == "yes"):
            tOrder.orderCustomerIsMember = True
        else:
            tOrder.orderCustomerIsMember = False
        
        #Paypal Info
        tOrder.orderTransactionId = tTransactionId
        
        tOrder.orderPaypalFirstName = tCustomerFirstName
        tOrder.orderPaypalLastName = tCustomerLastName
        
        tOrder.orderCost = float(tArgumentDic['payment_gross'])
        tOrder.orderCustomerPaypalId = tArgumentDic['payer_id']
        tOrder.orderPaypalEmail = str(tPaypalEmail).lower()
        
        tAssignedAgentNick = tPaypalOrder.GetAssignedAgent(tOrder)
        tOrder.orderAssignedAgent = tAssignedAgentNick
        #logging.debug("Order assigned to agent: " + str(tAssignedAgentNick))
        
        tOrder.orderReferralCode = tReferCode
        
        tOrder.orderDeliver = 'False'
        
        if(tOrder.orderVerificationCode == None or tOrder.orderVerificationCode == ''):
            tOrder.orderVerificationCode = re.sub(r'\W', '', str(uuid.uuid4())).lower()
                    
        tCurrentEocPrices = PriceContainer.GetCurrentPriceDic()
        tCurrent07Prices = PriceContainer.GetCurrentPriceDic07()        
        
        tSkip07 = False    
        if tOrder.orderSimpleGoldAmount in tCurrentEocPrices.keys():
            if str(tOrder.orderCost) == str(tCurrentEocPrices[tOrder.orderSimpleGoldAmount]):
                tOrder.orderGoldType = 'eoc'
                tSkip07 = True
        
        if not tSkip07:
            if tOrder.orderSimpleGoldAmount in tCurrent07Prices.keys():
                if str(tOrder.orderCost) == str(tCurrent07Prices[tOrder.orderSimpleGoldAmount]):
                    tOrder.orderGoldType = '07'         
        
        tOrderKey = str(tOrder.put())
        
        #logging.debug("Order Saved: " + str(tOrderKey))
        
        taskqueue.add(url="/iplookup", countdown = 1, params = {"ip":tOrderIp, "transid":tTransactionId} )

        tUsedBonus = []
        tCustomerList = tCustomerHandler.GetCustomerByPpid(tOrder.orderCustomerPaypalId)
        if (len(tCustomerList) == 1):
            tCustomer = tCustomerList[0]
            tIpList = tCustomer.customerIpAddresses
            tIpList.append(tOrderIp)
            tCustomer.customerIpAddresses = tIpList
            
            tOrderList = tCustomer.customerOrders
            tOrderList.append(tOrderKey)
            tCustomer.customerOrders = tOrderList
            
            tCustomer.customerOrderCount = int(tCustomer.customerOrderCount) + 1
            #tUsedBonus = tCustomer.customerUsedBonus
            tUsedBonus = Order.GetCustomerPromoCodes(tCustomer.customerPaypalId)
            
            #tOrder.orderCustomer = str(tCustomer.key())
        elif(len(tCustomerList) == 0):
            tCustomer.customerEmail = str(tOrder.orderPaypalEmail).lower()
            tCustomer.customerName = tCustomerName
            tCustomer.customerFirstName = tOrder.orderPaypalFirstName
            tCustomer.customerLastName = tOrder.orderPaypalLastName
            tCustomer.customerIpAddresses = [tOrderIp]
            tCustomer.customerOrders = [tOrderKey]
            tCustomer.customerOrderCount = 1
            tCustomer.customerPhone = tMobilePhone
            tCustomer.customerEmailVerified = False
            tCustomer.customerPhoneVerified = False
            tCustomer.customerIdVerified = False
            tCustomer.customerPaypalId = tOrder.orderCustomerPaypalId
            tCustomer.customerIsGlobalBlacklisted = False
            tCustomer.customerIsPaBlacklisted = False
            
        tPromoCode = ""
        tPromoCode = tOrder.orderPromotionalCode
        #logging.debug("Order Promo Code: " + str(tOrder.orderPromotionalCode))
        tPromo = Promo()
        tPromoCode = tPromoCode.lower()
        try:
            logging.debug("Promo Code: " + str(tPromoCode))
            tPromo = Promo.GetPromoByCode(tPromoCode)
            logging.debug("Promo: " + str(tPromo))
            tGoldAmount = tOrder.orderQuantity
            logging.debug("Gold Amount: " + str(tGoldAmount))
            logging.debug("Promo is active: " + str(tPromo.promoIsActive))
            
            if ((tPromo.promoIsActive) and (tPromo.promoUses <= tPromo.promoLimit)):
                if (tPromo.promoLimit != 0):
                    tPromo.promoUses = tPromo.promoUses + 1
                
                if((tPromoCode in tUsedBonus) == True):
                    tPercentBonus = 0.0
                else:
                    tPercentBonus = tGoldAmount * tPromo.promoPercentage
                    #tUsedBonus.append(tPromoCode)
    
                tGoldAmount = tGoldAmount + tPercentBonus
                tGoldAmount = tGoldAmount + tPromo.promoGoldAmount
                tTotalBonusFloat = tPercentBonus + tPromo.promoGoldAmount
                logging.debug("Bonus float: " + str(tTotalBonusFloat))
                tOrder.orderBonusQuantity = int(tTotalBonusFloat)
                    
                logging.debug("Total Bonus Float " + str(tTotalBonusFloat))
                logging.debug("Promo Gold Amount " + str(tPromo.promoGoldAmount))
                logging.debug("Promo Percentage " + str(tPercentBonus))
        except:
            tOrder.orderBonusQuantity = 0
            
        #tCustomer.customerUsedBonus = tUsedBonus
        
        tCustomerKey = str(tCustomer.put())
        tOrder.orderCustomer = tCustomerKey
        tOrderKey = str(tOrder.put())
    
        if (tCustomerName == ""):
            tCustomerName = tCustomerFirstName + " " + tCustomerLastName
        
        if(tGoldAmount == None or len(str(tGoldAmount)) == 0):
            tGoldAmount = tGoldAmountString
            
        response = taskqueue.add(url="/emailnotify", countdown = 1, 
                                 params = {"email":tPaypalEmail, "gold":tGoldAmount, 
                                "name":tCustomerName, 'key':tOrderKey} )
        logging.debug(str(response))
            
        #logging.debug("===========Paypal IPN Storage Finished===========")
    
    def ProcessSubscription(self, pArgumentDic):
        tVipSubscriber = VipSubscriber()
        tVipSub = VipSubscription()
        tVipPayment = VipPayment()
        tLogList = []
        
        tOwnerEmail = pArgumentDic['payer_email']
        tOwnerId = pArgumentDic['payer_id']
        tVipSubscriber = VipSubscriber.GetSubscriberByIdAndEmail(tOwnerId, tOwnerEmail)
        tVipSubs = VipSubscription.GetActiveSubscriptionsByOwner(tOwnerId)
        
        if (tVipSubs != None and len(tVipSubs) > 0):
            tVipSub = tVipSubs[0]
            tVipSub.subscriptionIsActive = True
            tLogList = tVipSub.subscriptionLog
            tLogList.append("Paid: " + str(datetime.datetime.now()) + " with transaction id " + pArgumentDic['txn_id'])
            tVipSub.subscriptionLog = tLogList
        else:
            tVipSub.subscriptionAutoState = "Tier0"
            tVipSub.subscriptionId = pArgumentDic['subscr_id']
            tLogList = tVipSub.subscriptionLog
            tLogList.append("Started: " + str(datetime.datetime.now()) + " with transaction id " + pArgumentDic['txn_id'])
            tVipSub.subscriptionLog = tLogList
            tVipSub.subscriptionNeedsUpgrade = True
            tVipSub.subscriptionOwner = tOwnerId
            
        tVipSub.subscriptionIsActive = True
        tSubKey = str(tVipSub.put())
        
        tVipSubscriber.subscriberHasActiveSubscription = True
        tVipSubscriber.subscriberActiveSubscription = tSubKey
        tSubList = []
        tSubList = tVipSubscriber.subscriberSubscriptions
        tSubList.append(tSubKey)
        tVipSubscriber.put()
        
        if('payment_gross' in pArgumentDic.keys()):
            tVipPayment.paymentAmount = pArgumentDic['payment_gross']
        
        tVipPayment.paymentEmail = tOwnerEmail
        tVipPayment.paymentPaypalId = tOwnerId
        tVipPayment.put()
    
    def ProcessSubscriptionCancellation(self, pArgumentDic):
        tVipSubscriber = VipSubscriber()
        tVipSub = VipSubscription()
        tVipPayment = VipPayment()
        tLogList = []
        
        tOwnerEmail = pArgumentDic['payer_email']
        tOwnerId = pArgumentDic['payer_id']
        
        tVipSubList = VipSubscription.GetActiveSubscriptionsByOwner(tOwnerId)
        
        if (tVipSubList != None):        
            if(len(tVipSubList) > 0):
                tVipSub = tVipSubList[0]
                tVipSub.subscriptionIsActive = False
                tVipSub.subscriptionEnd = datetime.datetime.now()
                tVipSub.subscriptionNeedsCancel = True
                tVipSub.put()
            
        tVipSubscriber.subscriberHasActiveSubscription = False
        tVipSubscriber.subscriberActiveSubscription = ""
        tVipSubscriber.put()
            
    def ProcessPlayerAuctions(self, pArgumentDic):
        tPaOrder = PaOrder()
        
        if ('mc_gross' in pArgumentDic.keys()):
            tPaOrder.paAmount = pArgumentDic['mc_gross']
        
        if ('payer_id' in pArgumentDic.keys()):
            tPaOrder.paTransactionId = pArgumentDic['payer_id']
            
        tPaOrder.put()
    
    def ProcessChargeback(self, pArgumentDic):
        tArgumentDic = {}
        tArgumentDic = pArgumentDic
        tCustomer = Customer()
        tCustomerHandler = CustomerHandler()
        if(tArgumentDic.has_key('payer_id')):
            tCustomer = tCustomerHandler.GetCustomerByPpid(tArgumentDic['payer_id'])[0]

        tSuccess = tCustomerHandler.PaBlacklistCustomer(str(tCustomer.key()))
        try:
            tPaypalEmail = tCustomer.customerEmail
            #logging.debug("Adding Chargeback Email for " + tPaypalEmail)
            taskqueue.add(url="/emailchargeback", countdown = 1, params = {"email":tPaypalEmail} )
        except:
            logging.debug("Failure Queueing Chargeback Email")
        
        if (tSuccess):
            logging.debug("Successfully PA Blacklisted " + str(tArgumentDic['payer_id']) + " due to Chargeback")
        else:
            logging.debug("Failure PA Blacklisting " + str(tArgumentDic['payer_id']))
    
    def GetAssignedAgent(self, pOrder = None):
        tAgent = Agent()
        tPaypal = PaypalOrder()
        tAgents = []
        Switch = {}
        tOrder = Order()
        tOrder = pOrder
        
        #Need to implement these methods
        #Switch[(1,2)] = tPaypal.UseFullAndBackupAgents
        #Switch[(0,2)] = tPaypal.UseBackupAgent
        #Switch[(2,2)] = tPaypal.UseFullAgent
        Switch[(0,0)] = tPaypal.AssignNoAgent
        Switch[(0,1)] = tPaypal.UseBackupAgent
        Switch[(1,0)] = tPaypal.UseFullAgent
        Switch[(1,1)] = tPaypal.UseFullAndBackupAgents
        Switch[(2,0)] = tPaypal.UseFullAgent
        Switch[(2,1)] = tPaypal.UseFullAndBackupAgents
        Switch[(3,0)] = tPaypal.UseFullAgent
        Switch[(3,1)] = tPaypal.UseFullAgent
        
        
        #Based on the raw online numbers of each group
        tCurrentState = (tPaypal.GetNumberofOnlineFullAgents(), tPaypal.GetNumberofOnlineBackupAgents())
        #logging.debug("Current State" + str(tCurrentState))
        
        #The end agent will be handled in each function
        tAgent = Switch[tCurrentState]()
        if (tOrder != None):
            try:
                #logging.debug("Agent Current Total: " + str(tAgent.agentCurrentOrderTotal))
                #logging.debug("Order Quantity: " + str(tOrder.orderQuantity))
                tAgent.agentCurrentOrderTotal = tAgent.agentCurrentOrderTotal + int(tOrder.orderQuantity)
                #logging.debug("New Agent Current Total: " + str(tAgent.agentCurrentOrderTotal))
                tAgent.agentNotify = True
                tAgent.put()
                #logging.debug("GetAssignedAgent returning agent: " + str(tAgent.agentId))
                return tAgent.agentId
            except:
                #logging.debug("Hit an error")
                return "No Agent Online"
        else:
            try:
                return str(tAgent.agentId)
            except:
                return "No Agent Online"
    
    def AssignNoAgent(self):
        #logging.debug("AssignNoAgent Called")
        return "No Agent Online"
    
    def UseBackupAgent(self):
        #logging.debug("UseBackupAgent Called")
        tAgent = Agent()
        tAgents = []
        tPaypal = PaypalOrder()
        tOnlineBackups = tPaypal.GetNumberofOnlineBackupAgents()
        tAvailableBackups = tPaypal.GetNumberofAvailableBackupAgents()
        #logging.debug("Online Backups: " + str(tOnlineBackups))
        #logging.debug("Available Backups: " + str(tAvailableBackups))
        
        if (tOnlineBackups > 0 and tAvailableBackups == 0):
            #logging.debug("Resetting Online Agents")
            tPaypal.ResetOnlineAgents()
        
        tAgents = tPaypal.GetAvailableBackupAgents()
        
        try:
            tAgent = tAgents[0]
            #logging.debug("UseBackupAgent Returning " + str(tAgent.agentId))
            return tAgent
        except:
            #logging.debug("Error in UseBackupAgent")
            return "No Agent Online"
        
    
    def UseFullAgent(self):
        tAgent = Agent()
        tAgents = []
        tPaypal = PaypalOrder()
        tOnlineAgents = tPaypal.GetNumberofOnlineFullAgents()
        tAvailableAgents = tPaypal.GetNumberofAvailableFullAgents()
        
        if (tOnlineAgents > 0 and tAvailableAgents == 0):
            tPaypal.ResetOnlineAgents()
            
        tAgents = tPaypal.GetAvailableFullAgents()
        
        try:
            tAgent = tAgents[0]
            return tAgent
        except:
            return "No Agent Online"
    
    def UseFullAndBackupAgents(self):
        tAgent = Agent()
        tAgents = []
        tPaypal = PaypalOrder()
        
        tOnlineBackups = tPaypal.GetNumberofOnlineBackupAgents()
        tAvailableBackups = tPaypal.GetNumberofAvailableBackupAgents()
        tOnlineAgents = tPaypal.GetNumberofOnlineFullAgents()
        tAvailableAgents = tPaypal.GetNumberofAvailableFullAgents()
    
        tTotalOnline = tOnlineAgents + tOnlineBackups
        tTotalAvailable = tAvailableAgents + tAvailableBackups
        
        if (tTotalOnline > 0 and tTotalAvailable == 0):
            tPaypal.ResetOnlineAgents()
            
        tAgents = tPaypal.GetAvailableAgents()
        try:
            tAgent = tAgents[0]
            return tAgent
        except:
            return "No Agent Online"
    
    def ReturnCleanNumber(self, pNumber):
        if (pNumber == 0):
            return 0
        elif(pNumber == 1):
            return 1
        elif(pNumber > 1):
            return 2
        else:
            return 0
        
    
    def ReturnCleanNumberBackup(self, pNumber):    
        if (pNumber == 0):
            return 0
        elif(pNumber >= 1):
            return 1
        else:
            return 0
    
    
    def GetOnlineAgents(self):
        FETCH_NUMBER = 30
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.order("-agentCurrentOrderTotal")
        tAgents = tAgentQuery.fetch(FETCH_NUMBER)
        return tAgents
    def GetNumberofOnlineAgents(self):
        tPaypal = PaypalOrder()
        tNumber = len(tPaypal.GetNumberofOnlineAgents()) 
        tNumber = tPaypal.ReturnCleanNumber(tNumber)
        return tNumber
    
    
    
    def GetAvailableAgents(self):
        FETCH_NUMBER = 30
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.filter("agentCurrentOrderTotal <", 30000000)
        tAgentQuery.order("-agentCurrentOrderTotal")
        tAgents = tAgentQuery.fetch(FETCH_NUMBER)
        return tAgents
    def GetNumberofAvailableAgents(self):
        tPaypal = PaypalOrder()
        tNumber = len(tPaypal.GetNumberofOnlineAgents())
        tNumber = tPaypal.ReturnCleanNumber(tNumber)
        return tNumber
        
    
    
    def GetAvailableFullAgents(self):
        FETCH_NUMBER = 30
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.filter("agentCurrentOrderTotal <", 30000000)
        tAgentQuery.filter("agentIsFullAgent", True)
        tAgentQuery.order("-agentCurrentOrderTotal")
        tAgents = tAgentQuery.fetch(FETCH_NUMBER)
        return tAgents
    def GetNumberofAvailableFullAgents(self):
        tPaypal = PaypalOrder()
        tNumber = len(tPaypal.GetAvailableFullAgents())
        tNumber = tPaypal.ReturnCleanNumber(tNumber)
        return tNumber
    
    
    def GetOnlineFullAgents(self):
        FETCH_NUMBER = 30
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.filter("agentIsFullAgent", True)
        tAgentQuery.order("-agentCurrentOrderTotal")
        tAgents = tAgentQuery.fetch(FETCH_NUMBER)
        return tAgents
    def GetNumberofOnlineFullAgents(self):
        tPaypal = PaypalOrder()
        tNumber = len(tPaypal.GetOnlineFullAgents())
        tNumber = tPaypal.ReturnCleanNumber(tNumber)
        return tNumber
        
    
    
    def GetOnlineBackupAgents(self):
        FETCH_NUMBER = 30
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.filter("agentIsFullAgent", False)
        tAgentQuery.order("-agentCurrentOrderTotal")
        tAgents = tAgentQuery.fetch(FETCH_NUMBER)
        return tAgents
    def GetNumberofOnlineBackupAgents(self):
        tPaypal = PaypalOrder()
        tNumber = len(tPaypal.GetOnlineBackupAgents())
        tNumber = tPaypal.ReturnCleanNumberBackup(tNumber)
        return tNumber
    
    
    
    def GetAvailableBackupAgents(self):
        FETCH_NUMBER = 30
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.filter("agentCurrentOrderTotal <", 30000000)
        tAgentQuery.filter("agentIsFullAgent", False)
        tAgentQuery.order("-agentCurrentOrderTotal")
        tAgents = tAgentQuery.fetch(FETCH_NUMBER)
        return tAgents
    def GetNumberofAvailableBackupAgents(self):
        tPaypal = PaypalOrder()
        tNumber = len(tPaypal.GetAvailableBackupAgents())
        tNumber = tPaypal.ReturnCleanNumberBackup(tNumber)
        return tNumber
    
    
    
    def ResetOnlineAgents(self):
        tPaypal = PaypalOrder()
        tAgents = tPaypal.GetOnlineAgents()
        for tAgent in tAgents:
            tAgent.agentCurrentOrderTotal = 0
            #logging.debug("Resetting total for agent: " + str(tAgent.agentId))
            tAgent.put()
            time.sleep(1)
        return 1
        
        

class PaypalAgentTest(webapp.RequestHandler):
    LOCATION = '../views/paypaltest.html'
    def GetContext(self):
        tContext = {}
        tPaypal = PaypalOrder()
        tOrderList = []
        
        tOrderAmounts = [1000000,2000000,5000000,10000000,
                         20000000,40000000,80000000,100000000]
        
        i = 1
        while(i < 21):
            i = i + 1
            tOrder = Order()
            tOrder.orderQuantity = choice(tOrderAmounts)
            tAgentId = tPaypal.GetAssignedAgent(tOrder)
            tOrder.orderAgent = tAgentId
            tOrderList.append(tOrder)
            
        tContext['orders'] = tOrderList
        
        return tContext        
        
        
    #def GetAssignedAgent(self, pOrder):
        #tOrder = Order()
        #tOrder = pOrder
        #tAgents = []
        #tAgent = Agent()
        
        #tAgentQuery = Agent.all()
        #tAgentQuery.filter("agentOnline", True)
        #tAgentQuery.order("agentCurrentOrderTotal")
        #tAgents = tAgentQuery.fetch(10)
        
        #try:
            #logging.debug("=========Begin Online Agents=========")
            #for tAgent in tAgents:
                #logging.debug("Found online agent: " + str(tAgent.agentId))
            #logging.debug("=========End Online Agents=========")
        #except:
            #logging.debug("Error retrieving online agents for assignment")
        
        #tAgentQuery = Agent.all()
        #tAgentQuery.filter("agentOnline", True)
        #tAgentQuery.filter("agentCurrentOrderTotal <", 30000000)
        #tAgentQuery.order("agentCurrentOrderTotal")
        #tAgents = tAgentQuery.fetch(10)
        
        #tFullAgents = [a for a in tAgents if a.agentIsFullAgent == True]
        
        #try:
            #logging.debug("=========Begin Open Agents=========")
            #for tAgent in tAgents:
                #logging.debug("Found open agent: " + str(tAgent.agentId) + 
                              #" Full agent status: " + str(tAgent.agentIsFullAgent))
            #logging.debug("=========End Open Agents=========")
        #except:
            #logging.debug("Error retrieving open agents for assignment")
        
        #if (len(tAgents) > 0 and len(tFullAgents) == 1):
            #tAgent = tAgents[0]
            #logging.debug("Selected Agent: " + str(tAgent.agentId))
            #if (tAgent.agentCurrentOrderTotal != None):
                #tAgent.agentCurrentOrderTotal = tAgent.agentCurrentOrderTotal + tOrder.orderQuantity
            #else:
                #tAgent.agentCurrentOrderTotal = tOrder.orderQuantity
            #logging.debug("Agent total is now: " + str(tAgent.agentCurrentOrderTotal))
            #tAgent.put()
            
            #return tAgent.agentId
        #elif (len(tAgents) > 0 and len(tFullAgents) > 1):
            ##logging.debug("No agents meet criteria, resetting")
            ##tAgentQuery = Agent.all()
            ##tAgentQuery.filter("agentOnline", True)
            ##tAgentQuery.filter("agentIsFullAgent", True)
            ##tAgents = tAgentQuery.fetch(20)
            
            ##for tAgent in tAgents:
                ##tAgent.agentCurrentOrderTotal = 0
                ##logging.debug("Resetting total for agent: " + str(tAgent.agentId))
                ##tAgent.put()
            
            #tAgentQuery = Agent.all()
            #tAgentQuery.filter("agentOnline", True)
            #tAgentQuery.filter("agentCurrentOrderTotal <", 30000000)
            #tAgentQuery.filter("agentIsFullAgent", True)
            #tAgentQuery.order("agentCurrentOrderTotal")
            #tAgents = tAgentQuery.fetch(10)
            
            #if (len(tAgents) > 0):
                #tAgent = tAgents[0]            
                #logging.debug("Selected Agent: " + str(tAgent.agentId))
                #if (tAgent.agentCurrentOrderTotal != None):
                    #tAgent.agentCurrentOrderTotal = tAgent.agentCurrentOrderTotal + tOrder.orderQuantity
                #else:
                    #tAgent.agentCurrentOrderTotal = tOrder.orderQuantity
                #logging.debug("Agent total is now: " + str(tAgent.agentCurrentOrderTotal))
                #tAgent.put()
                #return str(tAgent.agentId)
        #elif (len(tAgents) == 0):
            #logging.debug("No agents meet criteria, resetting")
            #tAgentQuery = Agent.all()
            #tAgentQuery.filter("agentOnline", True)
            #tAgents = tAgentQuery.fetch(20)
            
            #for tAgent in tAgents:
                #tAgent.agentCurrentOrderTotal = 0
                #logging.debug("Resetting total for agent: " + str(tAgent.agentId))
                #tAgent.put()
            
            #tAgentQuery = Agent.all()
            #tAgentQuery.filter("agentOnline", True)
            #tAgentQuery.filter("agentCurrentOrderTotal <", 30000000)
            #tAgentQuery.order("agentCurrentOrderTotal")
            #tAgents = tAgentQuery.fetch(10)
            
            #if (len(tAgents) > 0):
                #tAgent = tAgents[0]            
                #logging.debug("Selected Agent: " + str(tAgent.agentId))
                #if (tAgent.agentCurrentOrderTotal != None):
                    #tAgent.agentCurrentOrderTotal = tAgent.agentCurrentOrderTotal + tOrder.orderQuantity
                #else:
                    #tAgent.agentCurrentOrderTotal = tOrder.orderQuantity
                #logging.debug("Agent total is now: " + str(tAgent.agentCurrentOrderTotal))
                #tAgent.put()
                #return str(tAgent.agentId)
            
            #else:
                #return "No Agent"
                
class PaypalRefunds(webapp.RequestHandler):
    def post(self):
        tUrl = "https://api-3t.paypal.com/nvp"
        tPaypalPayload = {}        
        tPaypal = PaypalRefund()
        tAgent = Agent()
        tOrder = Order()
        tUser = users.get_current_user()
        
        tTransId = str(self.request.get('orderid'))
        
        tAgentEmail = str(tUser.email())
        tAgent = Agent().GetAgentByEmail(tAgentEmail)
        tRefundAgent = tAgentEmail
        
        tOrderQuery = Order.all()
        tOrderQuery.filter("orderTransactionId", tTransId)
        #logging.debug("Transaction id: " + tTransId)
        tOrder = tOrderQuery.get()
        
        if (tOrder.orderDeliver != 'True'):
                
            tPaypalPayload['METHOD'] = "RefundTransaction"
            tPaypalPayload['TRANSACTIONID'] = tTransId
            
            tPayloadEncoded = tPaypal.GeneratePayload(tPaypalPayload)
            
            request_cookies = mechanize.CookieJar()
            request_opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(request_cookies))
            request_opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
            mechanize.install_opener(request_opener)
            
            tResponse = mechanize.urlopen(url = tUrl, timeout = 25.0, data = tPayloadEncoded)
            #logging.debug("Mechanize Package")
            #logging.debug("Url: " + tUrl)
            #logging.debug("Data: " + str(tPaypalPayload))
            
            tResult = tResponse.read()
            #logging.debug(tResult)
            
            tOrder.orderIsRefunded = "True"
            tOrder.orderRefundAgent = tRefundAgent
            tOrder.orderLocked = "True"
            tOrder.orderRefundId = ""
            tOrder.put()
            
            self.response.out.write("Order Locked and Refunded")
                