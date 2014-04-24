from models.agent import Agent
from models.paorder import PaOrder

import logging, time

class DeliveryAssignment():
    
    def GetAssignedAgent(self, pOrder = None):
        tAgent = Agent()
        tAssignment = DeliveryAssignment()
        tAgents = []
        Switch = {}
        tOrder = PaOrder()
        tOrder = pOrder
        
        #Need to implement these methods
        #Switch[(1,2)] = tPaypal.UseFullAndBackupAgents
        #Switch[(0,2)] = tPaypal.UseBackupAgent
        #Switch[(2,2)] = tPaypal.UseFullAgent
        Switch[(0,0)] = tAssignment.AssignNoAgent
        Switch[(0,1)] = tAssignment.UseBackupAgent
        Switch[(1,0)] = tAssignment.UseFullAgent
        Switch[(1,1)] = tAssignment.UseFullAndBackupAgents
        Switch[(2,0)] = tAssignment.UseFullAgent
        Switch[(2,1)] = tAssignment.UseFullAndBackupAgents
        Switch[(3,0)] = tAssignment.UseFullAgent
        Switch[(3,1)] = tAssignment.UseFullAgent
        
        
        #Based on the raw online numbers of each group
        tCurrentState = (tAssignment.GetNumberofOnlineFullAgents(), tAssignment.GetNumberofOnlineBackupAgents())
        #logging.debug("Current State" + str(tCurrentState))
        
        #The end agent will be handled in each function
        tAgent = Switch[tCurrentState]()
        if (tOrder != None):
            try:
                #logging.debug("Agent Current Total: " + str(tAgent.agentCurrentOrderTotal))
                #logging.debug("Order Quantity: " + str(tOrder.paAmountInt))
                tAgent.agentCurrentOrderTotal = tAgent.agentCurrentOrderTotal + 1
                #logging.debug("New Agent Current Total: " + str(tAgent.agentCurrentOrderTotal))
                tAgent.agentNotify = True
                tAgent.put()
                #logging.debug("GetAssignedAgent returning agent: " + str(tAgent.agentId))
                return tAgent
            except:
                #logging.debug("Hit an error")
                return "No Agent Online"
        else:
            try:
                return tAgent
            except:
                return "No Agent Online"
    
    def AssignNoAgent(self):
        #logging.debug("AssignNoAgent Called")
        return "No Agent Online"
    
    def UseBackupAgent(self):
        #logging.debug("UseBackupAgent Called")
        tAgent = Agent()
        tAgents = []
        tPaypal = DeliveryAssignment()
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
        tPaypal = DeliveryAssignment()
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
        tPaypal = DeliveryAssignment()
        
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
        tPaypal = DeliveryAssignment()
        tNumber = len(tPaypal.GetNumberofOnlineAgents()) 
        tNumber = tPaypal.ReturnCleanNumber(tNumber)
        return tNumber
    
    
    
    def GetAvailableAgents(self):
        FETCH_NUMBER = 30
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.filter("agentCurrentOrderTotal <", 1)
        tAgentQuery.order("-agentCurrentOrderTotal")
        tAgents = tAgentQuery.fetch(FETCH_NUMBER)
        return tAgents
    def GetNumberofAvailableAgents(self):
        tPaypal = DeliveryAssignment()
        tNumber = len(tPaypal.GetNumberofOnlineAgents())
        tNumber = tPaypal.ReturnCleanNumber(tNumber)
        return tNumber
        
    
    
    def GetAvailableFullAgents(self):
        FETCH_NUMBER = 30
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.filter("agentCurrentOrderTotal <", 1)
        tAgentQuery.filter("agentIsFullAgent", True)
        tAgentQuery.order("-agentCurrentOrderTotal")
        tAgents = tAgentQuery.fetch(FETCH_NUMBER)
        return tAgents
    def GetNumberofAvailableFullAgents(self):
        tPaypal = DeliveryAssignment()
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
        tPaypal = DeliveryAssignment()
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
        tPaypal = DeliveryAssignment()
        tNumber = len(tPaypal.GetOnlineBackupAgents())
        tNumber = tPaypal.ReturnCleanNumberBackup(tNumber)
        return tNumber
    
    
    
    def GetAvailableBackupAgents(self):
        FETCH_NUMBER = 30
        tAgentQuery = Agent.all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.filter("agentCurrentOrderTotal <", 1)
        tAgentQuery.filter("agentIsFullAgent", False)
        tAgentQuery.order("-agentCurrentOrderTotal")
        tAgents = tAgentQuery.fetch(FETCH_NUMBER)
        return tAgents
    def GetNumberofAvailableBackupAgents(self):
        tPaypal = DeliveryAssignment()
        tNumber = len(tPaypal.GetAvailableBackupAgents())
        tNumber = tPaypal.ReturnCleanNumberBackup(tNumber)
        return tNumber
    
    
    
    def ResetOnlineAgents(self):
        tPaypal = DeliveryAssignment()
        tAgents = tPaypal.GetOnlineAgents()
        for tAgent in tAgents:
            tAgent.agentCurrentOrderTotal = 0
            #logging.debug("Resetting total for agent: " + str(tAgent.agentId))
            tAgent.put()
            time.sleep(1)
        return 1