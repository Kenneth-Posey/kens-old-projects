
import os, logging, random, urllib
from customerhandler import CustomerHandler
from models.customer import Customer
from google.appengine.api import memcache, users, mail
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

class VerifyEmail(webapp.RequestHandler):
    def post(self):
        pEmail = self.request.get('email')
        pCustomerId = self.request.get('custid')
        pMarkVerified = self.request.get('verified')
        
        #logging.debug(str(pEmail))
        #logging.debug(str(pCustomerId))
        #logging.debug(str(pMarkVerified))
        
        tCustomer = Customer.get(pCustomerId)
        tNumber = random.randint(200, 999)
        
        if(pMarkVerified != None and pMarkVerified == 'True'):
            tCustomer.customerEmailVerified = True
            tCustomer.put()
                
            self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
            self.response.headers['Content-Type'] = 'Content-Type: plain/text'
            self.response.out.write("Verified")
        else:
            tMessage = "Verification Number: " + str(tNumber)
            mail.send_mail(sender = "Smokin Mils Goldshop <Support@eMeMO.com>",
                           to = pEmail,
                           subject = "Smokin Mils Goldshop Email Verification",
                           body = tMessage)
            #logging.debug("Sent Verification Email to : " + pEmail + " Number: " + str(tNumber))
            tCustomer.customerEmailVerificationNumber = str(tNumber)
            tCustomer.put()
                
            self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
            self.response.headers['Content-Type'] = 'Content-Type: plain/text'
            self.response.out.write("New: " + str(tNumber))
            