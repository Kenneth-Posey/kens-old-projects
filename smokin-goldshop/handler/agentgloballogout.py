
import os, logging, datetime
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from base import BaseHandler

from models.agent import Agent

class AgentGlobalLogout(BaseHandler):
    def post(self):
        tAgentQuery = Agent().all()
        tAgentList = tAgentQuery.fetch(100)
        agent = Agent()
        
        for agent in tAgentList:
            agent.agentOnline = False
            agent.put()
        
        self.response.out.write("Success")