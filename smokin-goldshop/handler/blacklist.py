
import os, logging, random, urllib
from customerhandler import CustomerHandler
from models.customer import Customer
from google.appengine.api import memcache, users, urlfetch
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

from customerhandler import CustomerHandler
from models.customer import Customer

class Blacklist(webapp.RequestHandler):
    def post(self):
        #logging.debug("starting")
        #logging.debug(str(self.request))
        tCustomerHandler = CustomerHandler()
        tCustomer = Customer()

        pBlacklistType = self.request.get('BlackListType')    
        pCustomerId = self.request.get('custid')        
        
        tRequest = self.request        
        
        #logging.debug("Beginning Blacklist of type " + pBlacklistType + " for customer " + pCustomerId)
        
        self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
        self.response.headers['Content-Type'] = 'Content-Type: plain/text'
        
        if(pBlacklistType == 'PA'):
            tCustomerHandler.PaBlacklistCustomer(pCustomerId)
            #logging.debug("Blacklisted PA")
            self.response.out.write("PA Blacklisted!")
        elif(pBlacklistType == 'Global'):
            tCustomerHandler.GlobalBlacklistCustomer(pCustomerId)
            #logging.debug("Blacklisted Global")
            self.response.out.write("Global Blacklisted!")
        else:
            #logging.debug("Error Blacklisting")
            self.response.out.write("Error Blacklisting")
    
    