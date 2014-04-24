from google.appengine.ext import db
from agent import Agent
import uuid, re

class Order(db.Expando):
    orderCreated = db.DateTimeProperty(auto_now_add = True)
    orderCompleted = db.DateTimeProperty(auto_now = True)
    orderIsGenerated = db.BooleanProperty(default=False)
    
    #Info from goldshop form
    orderIp = db.StringProperty()
    orderFormEmail = db.StringProperty()
    orderAccountName = db.StringProperty()
    orderQuantity = db.IntegerProperty()
    orderBonusQuantity = db.IntegerProperty()
    orderSimpleGoldAmount = db.StringProperty()
    orderGoldType = db.StringProperty()
    orderPromotionalCode = db.StringProperty()
    orderFormName = db.StringProperty()
    orderCustomerIsMember = db.BooleanProperty()
    orderCombatLevel = db.StringProperty()
    
    #info from paypal
    orderTransactionId = db.StringProperty()
    orderPaypalStatus = db.StringProperty()
    orderPaypalEmail = db.StringProperty()
    orderCost = db.FloatProperty()
    orderPaymentMethod = db.StringProperty()
    orderPaypalId = db.StringProperty()
    orderChargeback = db.BooleanProperty()
    orderPaypalFirstName = db.StringProperty()
    orderPaypalLastName = db.StringProperty()
    
    #info from the backend
    orderDeliver = db.StringProperty()
    orderLocked = db.StringProperty()
    orderCustomer = db.StringProperty()
    orderCustomerPaypalId = db.StringProperty()
    orderClaimed = db.BooleanProperty()
    orderAgent = db.StringProperty()
    orderDeliveryAgent = db.StringProperty()
    orderAssignedAgent = db.StringProperty()
    orderAgentGold = db.BooleanProperty()
    orderCommission = db.FloatProperty()
    orderEmailNumber = db.StringProperty()
    orderSmsNumber = db.StringProperty()
    
    #refund info
    orderRefundAgent = db.StringProperty()
    orderRefundId = db.StringProperty()
    orderIsRefunded = db.StringProperty()
    
    #referral info
    orderReferralCode = db.StringProperty()
    orderReferralAmount = db.FloatProperty()
    
    orderIsVerified = db.BooleanProperty(default=False)
    orderVerificationCode = db.StringProperty()
    
    #Deprecated
    orderMobileNumber = db.StringProperty()
    orderSimpleBonusGold = db.StringProperty()
    
    
    @staticmethod
    def GetCustomerPromoCodes(pCustomerId):
        tOrder = Order()
        tOrders = []
        tCodes = []
        
        tOrderQuery = Order.all()
        tOrderQuery.filter("orderCustomerPaypalId", pCustomerId)
        tOrderQuery.filter("orderDeliver", "True")
        tOrders = tOrderQuery.fetch(limit=50)
        if(tOrders != None and len(tOrders) > 0):
            for tOrder in tOrders:
                tCodes.append(tOrder.orderPromotionalCode)
            tUniqueCodes = [c for c in set(tCodes)]
            
            return tUniqueCodes
        else:
            
            return []
        
        
    def GetAssignedAgentNick(self):
        tAgent = Agent()
        pAgentEmail = self.orderAssignedAgent
        tAgent = Agent.GetAgentByEmail(pAgentEmail)
        tAgentNick = tAgent.agentNickName
        return tAgentNick
    
    def GetDeliveryAgentNick(self):
        tAgent = Agent()
        pAgentEmail = self.orderDeliveryAgent
        tAgent = Agent.GetAgentByEmail(pAgentEmail)
        tAgentNick = tAgent.agentNickName
        return tAgentNick