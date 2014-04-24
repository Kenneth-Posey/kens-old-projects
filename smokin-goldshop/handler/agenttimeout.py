
import os, logging, datetime
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from base import BaseHandler

from models.agent import Agent
from agenthandler import AgentHandler

class AgentTimeout(BaseHandler):
    def get(self):
        tAgent = Agent()
        tAgentsOnline = []
        
        tCurrentTime = datetime.datetime.now()
        tIncrement = datetime.timedelta(minutes = -30)
        tTime = tIncrement + tCurrentTime
        
        tAgentQuery = Agent().all()
        tAgentQuery.filter("agentOnline", True)
        tAgentQuery.filter("agentLastActive <", tTime)
        
        tAgentsOnline = tAgentQuery.fetch(10)

        if (len(tAgentsOnline) > 0):
            for tAgent in tAgentsOnline:
                tAgent.agentOnline = False
                tAgent.put()
                
                #logging.debug("Offlined " + tAgent.agentId + " for being inactive since " + str(tAgent.agentLastActive))
                
    def post(self):
        tAgent = Agent()
        tUser = users.get_current_user()
        if (tUser):
            tAgent = Agent().GetAgentByEmail(tUser.email())
            tAgent.put()
            #logging.debug("Action by Agent: " + tUser.email())
            if (tAgent.agentOnline == False):
                self.response.out.write("offline")
            else:
                self.response.out.write("online")
            