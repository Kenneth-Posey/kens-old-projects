from google.appengine.ext import db
import logging

class Agent(db.Expando):
    agentId = db.StringProperty()
    agentNickName = db.StringProperty(default = "")
    agentOrders = db.StringListProperty(default=[])
    agentPaOrders = db.StringListProperty(default=[]) #deprecated
    agentManualPaOrders = db.StringListProperty(default=[])
    agentManualStockChanges = db.StringListProperty(default=[])
    
    agentCurrentCommission = db.FloatProperty(default=0.0) 
    agentTotalCommission = db.FloatProperty(default=0.0) 
    
    agentLastActive = db.DateTimeProperty(auto_now = True)
    
    agentOnline = db.BooleanProperty(default=False)
    agentNotify = db.BooleanProperty(default=False)
    agentIsAdmin = db.BooleanProperty(default=False)
    agentIsEnabled = db.BooleanProperty(default=False)
    agentIsFullAgent = db.BooleanProperty(default=False)
        
    agentGoldSupply = db.IntegerProperty(default=0) #deprecated
    agentGoldSupplyEoc = db.IntegerProperty(default=0)
    agentGoldSupply07 = db.IntegerProperty(default=0)
    agentCurrentOrderTotal = db.IntegerProperty(default=0) 
    
    agentSoundPreference = db.StringProperty(default='True')
    agentSoundSelection = db.StringProperty(default='')
    agentSoundRepeat = db.IntegerProperty(default=1)
    agentSoundDelay = db.IntegerProperty(default=10000)
    
    
    @staticmethod
    def GetAgentByEmail(pEmail):
        tAgentQuery = None
        tAgentQueryString = None
        tAgentResults = []
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentId", str(pEmail))
        tAgentResults = tAgentQuery.fetch(1)
        try:
            tAgentResult = tAgentResults[0]
        except:
            #logging.error("Agent Email Not Found: " + str(pEmail))
            tAgentResult = Agent()
            tAgentResult.agentNickName = "No Agent"
            tAgentResult.agentId = "No Agent"
        return tAgentResult
    
    @staticmethod
    def GetAgentStatus(pEmail):
        tAgent = Agent().GetAgentByEmail(pEmail)[0]
        tStatus = tAgent.agentOnline
        return tStatus