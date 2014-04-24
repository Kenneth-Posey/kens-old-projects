
import os
import logging
from models.order import Order
from google.appengine.api import memcache, users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

from models.agent import Agent
from models.donorrecord import DonorRecord
from base import BaseHandler

class AgentMaster(BaseHandler):
    LOCATION = '../views/agentmaster.html'
    def GetContext(self):
            
        tAgent = Agent()
        tAgentList = []
        tAgentOrders = []
        tAgentDonations = []
        tAgentRequest = self.request.get('agent')
        context = {}
        
        tAgentList = Agent.all()
        context['agents'] = tAgentList
        if (tAgentRequest != ""):
            tAgent = Agent.get(tAgentRequest)
            
            tAgentOrdersQuery = Order.all()
            tAgentOrdersQuery.filter('orderAgent', str(tAgentRequest))
            tAgentOrdersQuery.order('-orderCompleted')
            tAgentOrders = tAgentOrdersQuery.fetch(100)
            
            tAgentDonorsQuery = DonorRecord.all()
            tAgentDonorsQuery.filter('donorAgent', tAgent.agentId)
            tAgentDonorsQuery.order('-donorDate')
            tAgentDonations = tAgentDonorsQuery.fetch(100)
            
            #logging.debug("Agent Order Count: " + str(len(tAgentOrders)))
            #logging.debug("Agent Donation Count: " + str(len(tAgentDonations)))
            
            context['agent'] = tAgent
            context['orders'] = tAgentOrders
            context['donations'] = tAgentDonations
            context['extended'] = 'True'
            
        return context