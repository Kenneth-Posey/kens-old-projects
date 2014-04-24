
import os, datetime, logging
from google.appengine.api import memcache, users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

from models.agent import Agent
from models.donorrecord import DonorRecord

from base import BaseHandler

class AgentHandler(BaseHandler):
    LOCATION = "../views/agent.html"
    def GetContext(self):
        return {}
    
    def PostContext(self):
        
        tUser = self.GetUser()
        tDonor = DonorRecord()
        
        tDonatorRsName = self.request.get('name')
        #logging.debug("Quantity Entered: " + str(self.request.get('quantity')))
        tDonatorAmount = int(self.request.get('quantity'))
        tDonatorNote = self.request.get('memo')
        tDonatorForumName = self.request.get('fname')
        tFormEmail = self.request.get('email')
        tAgentGold = self.request.get('agentgold')
        
        tDonor.donorAgent = tUser.email()
        tDonor.donorForumName = tDonatorForumName
        tDonor.donorMemo = tDonatorNote
        tDonor.donorRsName = tDonatorRsName
        tDonor.donorGoldAmount = int(tDonatorAmount)
        tDonor.put()
        
        tAgent = Agent()
        try:
            if (len(tFormEmail) > 0):
                tAgent = Agent().GetAgentByEmail(tFormEmail)
            else: 
                tAgent = Agent().GetAgentByEmail(str(tUser.email()))
        except:
            tAgent = Agent().GetAgentByEmail(str(tUser.email()))
        
        if (tAgent.agentGoldSupply == None):
            tAgent.agentGoldSupply = 0
            
        if (tDonatorAmount < 0):
            #logging.debug(str(tAgentGold))
            tDonatorAmount = tDonatorAmount / 1000000.0
            if (tAgentGold == 'on'):
                tCommission = tDonatorAmount * 0.65 * -1.0
            else:
                tAgent.agentGoldSupply += int(tDonatorAmount * 1000000.0)
                tCommission = tDonatorAmount * 0.05 * -1.0
            #logging.debug("Agent Commission: " + str(tDonatorAmount * -1.0))
            tAgent.agentCurrentCommission += tCommission
            tAgent.agentTotalCommission += tCommission
        else:
            tAgent.agentGoldSupply += tDonatorAmount
            
        tAgent.put()
        
        return {}
        
        
    
    
        
                    