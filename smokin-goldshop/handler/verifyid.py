
import os, logging, random, urllib
from customerhandler import CustomerHandler
from models.customer import Customer
from google.appengine.api import memcache, users, mail
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

class VerifyId(webapp.RequestHandler):
    def post(self):
        pEmail = self.request.get('email')
        pCustomerId = self.request.get('custid')
        pMarkVerified = self.request.get('verified')
        
        #logging.debug(str(pEmail))
        #logging.debug(str(pCustomerId))
        #logging.debug(str(pMarkVerified))
        
        tCustomer = Customer()
        tCustomer = Customer.get(pCustomerId)
        
        if(pMarkVerified != None and pMarkVerified == 'True'):
            tCustomer.customerIdVerified = True
            tCustomer.put()
                
            self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
            self.response.headers['Content-Type'] = 'Content-Type: plain/text'
            self.response.out.write("Verified")