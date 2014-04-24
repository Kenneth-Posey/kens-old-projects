
import os, logging, datetime
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from base import BaseHandler

from models.agent import Agent
from agenthandler import AgentHandler

class AgentOrderNotification(BaseHandler):
    def get(self):
        tAgent = Agent()
        tUser = users.get_current_user()
        if (tUser):
            tAgent = Agent().GetAgentByEmail(tUser.email())
            if(tAgent.agentOnline == True):
                if (tAgent.agentNotify == True):
                    tAgent.agentNotify = False
                    tAgent.put()
                    self.response.out.write("1")
                elif (tAgent.agentNotify == False):
                    self.response.out.write("0")
                else:
                    self.response.out.write("0")
                    tAgent.agentNotify = False
                    tAgent.put()
            else:
                self.response.out.write("2")
                