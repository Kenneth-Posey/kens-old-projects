
import os, logging, datetime
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from base import BaseHandler

from models.agent import Agent

class AgentLogging(BaseHandler):
    def post(self):
        tUser = users.get_current_user()
        tAgent = Agent().GetAgentByEmail(tUser.email())
        tStatus = tAgent.agentOnline
        
        if (tStatus == False):
            tAgent.agentOnline = True
            tAgent.agentCurrentOrderTotal = 100
            tReturn = "You're Online!"
        else:
            tAgent.agentOnline = False
            tReturn = "You're Offline!"
            
        tAgent.put()
        
        self.response.out.write(tReturn)
        exit
    
    def get(self):
        tAgentQuery = Agent().all()
        tAgentQuery.filter('agentOnline', True)
        
        tAgents = tAgentQuery.fetch(10)
        if (len(tAgents) > 0):
            self.response.out.write(str(len(tAgents)))
        else:
            self.response.out.write(str(0))
        exit
    
            