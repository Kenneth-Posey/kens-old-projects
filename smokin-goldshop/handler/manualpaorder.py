
import os, urllib, logging, datetime, re

from _numbertogp import NumberToGp
    
from models.ipinfo import IpInfo
from models.order import Order
from models.agent import Agent
from models.promo import Promo
from models.manualpaorder import ManualPaOrder
from models.customer import Customer
from models.stockaccount import StockAccount
from stockaccountmanager import StockAccountManager
from stockmanager import StockManager

from base import BaseHandler

class ManualPaOrderHandler(BaseHandler):
    LOCATION = "../views/manage-pa.html"
    def GetContext(self):
        
        tUser = self.GetUser()        
        
        tAllAgentList = []
        tAllPaOrderList = []
        
        tPaOrder = ManualPaOrder()
        
        tStringOffset = self.request.get('offset')
        #logging.debug('Offset string: {}'.format(tStringOffset))
        if (len(tStringOffset) > 0):
            tOffset = int(tStringOffset)
        else:
            tOffset = 0
        
        tNextIncrement = tOffset + 20
        if tOffset < 20:
            tPriorIncrement = 0
        else:
            tPriorIncrement = tOffset - 20
        
        #tOrderData = {}
        
        #Get date 30 days ago
        #tStartDate = datetime.datetime.now()
        #tIncrement = datetime.timedelta(days = -30)
        #tEndDate = tStartDate + tIncrement
                
        #logging.debug(str(tCustomerKey))
        tOrderQuery = ManualPaOrder.all()
        tOrderQuery.filter("orderIsGenerated", False)
        tOrderQuery.order("-orderCreated")
        tAllPaOrderList = tOrderQuery.fetch(20, offset=tOffset)
        #logging.debug(str(tCustomerOrders))
                    
        return {
            'offset'    :   tOffset,
            'next'      :   tNextIncrement,
            'prev'      :   tPriorIncrement,
            'orderlist' :   tAllPaOrderList
        }   
        
    def PostContext(self):
                
        tNewOrder = ManualPaOrder()
        tAgent = Agent()
        tPromo = Promo()
        
        tUserEmail = self.GetUser().email()
        
        tStockAccount = StockAccount()
        tStockManager = StockManager()
        tStockManager.LoadAccounts()
        
        tAgent = Agent().GetAgentByEmail(tUserEmail)
        logging.debug('Agent ' + str(tAgent.agentNickName))
                
        tPromoCode = self.request.get('promocode').lower().lstrip().rstrip()
        tPromoCode = tPromoCode.lower().lstrip().rstrip()
        
        tGoldType = str(self.request.get('type')).lower().lstrip().rstrip()
        tGoldAmountWeb = str(self.request.get('amount')).lower()
        tGoldAmountPretty = re.sub(r'[^0-9kmb]*','', tGoldAmountWeb)
        tGoldMatches = re.match(r'^[0-9]*(k|m|b{1})$', tGoldAmountPretty)
        if tGoldMatches is None:
            return {'error' : str(tGoldAmountWeb) + ' is an invalid gold amount'}
        
        tGoldValue = str(self.request.get('value')).lower()
        tGoldValue = float(re.sub(r'[^0-9\.*]*', '', tGoldValue))
        
        tPaId = self.request.get('paid').lower().lstrip().rstrip()
        
        if (tGoldType in ('eoc', '07')) is not True:
            return {'error' : str(tGoldType) + ' is an invalid gold type' }
                
        if not tGoldValue >= 0.0:
            return {'error' : str(tGoldValue) + ' is an invalid gold value'}
        
        tStringOffset = self.request.get('offset')
        if (len(tStringOffset) > 0):
            tOffset = int(tStringOffset)
        else:
            tOffset = 0        
                
        tNewOrder.orderOwner = tUserEmail
        
        tGoldAmount = NumberToGp.ConvertBetToInt(tGoldAmountPretty)
        
        tUsedBonus = []
        try:
            #logging.debug("Promo Code: " + str(tPromoCode))
            tPromo = Promo.GetPromoByCode(tPromoCode)
            #logging.debug("Promo: " + str(tPromo))
            #logging.debug("Gold Amount: " + str(tGoldAmount))
            #logging.debug("Promo is active: " + str(tPromo.promoIsActive))
            
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
                #logging.debug("Bonus float: " + str(tTotalBonusFloat))
                tPromoGoldAmount = int(tTotalBonusFloat)
                    
                #logging.debug("Total Bonus Float " + str(tTotalBonusFloat))
                #logging.debug("Promo Gold Amount " + str(tPromo.promoGoldAmount))
                #logging.debug("Promo Percentage " + str(tPercentBonus))
        except:
            tPromoGoldAmount = 0        
        
        tOrderTotalAmount = int(tGoldAmount) + int(tPromoGoldAmount)
        #logging.debug('Order gold ' + str(tOrderTotalAmount))
        
        logging.debug("{}".format(tOrderTotalAmount))
        logging.debug("{}".format(tGoldType))
        tStockManager.PlaceOrder(tOrderTotalAmount * -1, tGoldType)
        
        #if tGoldType == '07':
            ##logging.debug('07 detected')
            #tStockManager.PlaceOrder(aGoldQua
            #tStockAccountManager.Set07Stock(int(tOrderTotalAmount * -1))
            ##tAgent.agentGoldSupply07 = int(tAgent.agentGoldSupply07) - tOrderTotalAmount
        #elif tGoldType == 'eoc':
            ##logging.debug('eoc detected')
            ##tStockAccountManager.SetEOCStock(int(tOrderTotalAmount * -1))
            ##tAgent.agentGoldSupplyEoc = int(tAgent.agentGoldSupplyEoc) - tOrderTotalAmount
            
        #logging.debug('Agent 07 ' + str(tAgent.agentGoldSupply07))
        #logging.debug('Agent eoc ' + str(tAgent.agentGoldSupplyEoc))        
            
        tCommission = float(tGoldValue) * 0.05 + 0.50
        
        if tCommission >= 10.0:
            tCommission = 10.0
        
        tNewOrder.orderCashValue = float(tGoldValue)
        tNewOrder.orderOwner = tUserEmail
        tNewOrder.orderGoldAmount = int(tGoldAmount)
        tNewOrder.orderGoldAmountPretty = tGoldAmountPretty
        tNewOrder.orderGoldType = tGoldType
        tNewOrder.orderPaId = tPaId
        tNewOrder.orderPromoCode = tPromoCode
        tNewOrder.orderPromoGoldAmount = tPromoGoldAmount
        tNewOrderGuid = tNewOrder.put()
        
        tAgent.agentCurrentCommission = float(tAgent.agentCurrentCommission + tCommission)
        tAgent.agentTotalCommission = float(tAgent.agentTotalCommission + tCommission)
        tAgent.agentManualPaOrders = tAgent.agentManualPaOrders + [str(tNewOrderGuid)]
        tAgent.put()
        
        if int(tOffset) > 0:
            self.LOCATION = '/palist?offset=' + str(tOffset)
        else:
            self.LOCATION = '/palist'
            
        self.REDIRECT = True
        return {} 
        
        
        
        
        
        
        
        
        
        
        