import urllib, logging

from base import BaseHandler
from models.paorder import PaOrder
from models.agent import Agent
from google.appengine.ext import webapp
from google.appengine.api import users

class PaOrderView(BaseHandler):
    LOCATION = "../views/paorder.html"
    def GetContext(self):
        tContext = {}
        tVipList = []
        
        tPaKey = urllib.unquote(self.request.get('key'))
        if(tPaKey != None and len(tPaKey) > 0):
            tPaOrder = PaOrder.get(tPaKey)
            
            if(tPaOrder.paOrderDeliver == None):
                tPaOrder.paOrderDeliver = False
            
            if(tPaOrder.paOrderLock == None):
                tPaOrder.paOrderLock = False
            
            tContext['tPaOrder'] = tPaOrder
        return tContext
    
    
class DeliverPaOrder(webapp.RequestHandler):
    def post(self):
        tOrderKey = self.request.get('orderid')
        
        #logging.debug("tOrderKey: " + tOrderKey)
        
        tPaOrder = PaOrder()
        tPaOrder = PaOrder.get(tOrderKey)
        
        tUser = users.get_current_user()
        tAgent = Agent().GetAgentByEmail(str(tUser.email()))
        
        if (tPaOrder.paOrderDeliver == False and tPaOrder.paOrderLock == False and tAgent.agentIsEnabled == True):
            tGoldAmount = tPaOrder.paAmountInt
            
            tGoldAmountLong = tGoldAmount
            tGoldAmount = tGoldAmount / 1000000
            
            if (tAgent.agentGoldSupply == None):
                tAgent.agentGoldSupply = 0
            
            tCommission = tGoldAmount * 0.05 + 0.50
            
            tAgent.agentGoldSupply = int(tAgent.agentGoldSupply) - int(tGoldAmountLong)
            tAgent.agentCurrentCommission = tAgent.agentCurrentCommission + tCommission
            tAgent.agentTotalCommission = tAgent.agentTotalCommission + tCommission
            
            tAgentOrders = tAgent.agentOrders #Add order to agent pa orders
            tAgentOrders.append(tOrderKey)
            tAgent.agentOrders = tAgentOrders           
            
            tAgent.agentCurrentOrderTotal = tAgent.agentCurrentOrderTotal + 1
            
            tAgentKey = tAgent.put()
            
            tPaOrder.paDeliveryAgent = str(tAgent.agentId)
            tPaOrder.paDeliveryAgentNick = tAgent.agentNickName
            tPaOrder.paOrderDeliver = True
            tPaOrder.paOrderLock = True
            tKey = tPaOrder.put()
            
            #logging.debug("Delivery by Agent: " + str(tAgentKey))
            #logging.debug("Delivery of Order: " + str(tKey))
            
            self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
            self.response.headers['Content-Type'] = 'Content-Type: plain/text'
            self.response.out.write("Order Delivered")
        else:
            #logging.debug('Attempted to Deliver ' + tOrderKey + " by Agent " + tAgent.agentId)
            self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
            self.response.headers['Content-Type'] = 'Content-Type: plain/text'
            self.response.out.write("Order Not Deliverable")    