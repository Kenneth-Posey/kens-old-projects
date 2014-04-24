
import os, logging, re, cgi, urllib

from _numbertogp import NumberToGp

from public import mechanize
from google.appengine.api import memcache, users, urlfetch
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from models.agent import Agent
from base import BaseHandler

class AgentAccount(BaseHandler):
    LOCATION = "../views/agentaccount.html"
    def GetContext(self):
        tContext = {}
        if (self.IsUserAdmin()):
            tAgentsQuery = Agent().all()
            tAgentsQuery.order("agentNickName")
            tAgentsQuery.filter("agentIsEnabled", True)
            tAgents = tAgentsQuery.fetch(100)
            
            tAgent = Agent()
            for tAgent in tAgents:
                tAgent.__setattr__('agentGoldSupplyEocString', NumberToGp.ConvertIntToBet(tAgent.agentGoldSupplyEoc))
                tAgent.__setattr__('agentGoldSupply07String', NumberToGp.ConvertIntToBet(tAgent.agentGoldSupply07))
            
            tContext['agents'] = tAgents
            return tContext
        else:
            self.redirect("/")
            
    def PostContext(self):
        tContext = {}
        if (self.IsUserAdmin()):
            try:
                tAgentKey = self.request.get('custid')
                tAgent = Agent()
                tAgent = Agent().get(tAgentKey)
                tAgent.agentCurrentCommission = 0.0
                tAgent.put()
                self.response.out.write("Success")
            except:
                self.response.out.write("Error")
            tContext['nowrite'] = True
        return tContext
        