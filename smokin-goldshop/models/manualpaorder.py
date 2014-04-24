from google.appengine.ext import db
from agent import Agent
import logging

class ManualPaOrder(db.Expando):
    orderCreated = db.DateTimeProperty(auto_now_add = True)
    orderIsGenerated = db.BooleanProperty(default=False)
    
    orderOwner = db.StringProperty(default='')
    
    orderPromoCode = db.StringProperty(default='')
    orderPromoGoldAmount = db.IntegerProperty(default=0)
    
    orderGoldType = db.StringProperty(default='UNKNOWN') #eoc or 07
    orderGoldAmount = db.IntegerProperty(default=0)
    orderGoldAmountPretty = db.StringProperty(default='')
    
    orderPaId = db.StringProperty(default='')
    
    orderCashValue = db.FloatProperty(default=0.0)
    #orderComments = db.StringProperty(default='', multiline=True)
    
    
    def GetDeliveryAgentNick(self):
        tAgent = Agent()
        pAgentEmail = self.orderOwner
        tAgent = Agent.GetAgentByEmail(pAgentEmail)
        tAgentNick = tAgent.agentNickName
        return tAgentNick    