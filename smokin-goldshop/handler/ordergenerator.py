import random, urllib, os, logging
from public import mechanize    
from google.appengine.api import memcache, users, urlfetch, taskqueue, mail
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import Request, RequestHandler
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

from models.currenttimestamp import CurrentTimestamp
from _data import PriceContainer
from models.order import Order
from base import BaseHandler


class RandomOrderGenerator(BaseHandler):
    LOCATION = "../views/ordergen.html"
    def GetContext(self):
        tOrder = {}
        tContext = {}
        
        tOrderQuery = Order().all()
        tOrderQuery.filter("orderIsGenerated", True)
        tOrderQuery.order("-orderCreated")
        tOrderList = tOrderQuery.fetch(limit=30)
        
        tContext['orders'] = tOrderList
        
        return tContext
        
    def PostContext(self):
        tOrder = {}
        tContext = {}
        tPriceDictionary = PriceContainer.GetCurrentPriceDic()
        
        tType = str(self.request.get('type'))
        #logging.debug("Type: " + tType)
        
        tRandomAmount = ""
        tRandomPrice = ""
        tRandomAmount = random.choice(tPriceDictionary.keys())
        tRandomPrice = tPriceDictionary[tRandomAmount]
        tRandomNumberList = [str(random.randrange(0,9)) for i in range(0,9)]
        
        #valid for all types of orders
        tOrder['mc_currency'] = 'USD'
        tOrder['receiver_email'] = 'smokin.elite@gmail.com'
        tOrder['receiver_id'] = 'NSKCXUXQEMPBG'
        tOrder['residence_country'] = 'US'
        tOrder['address_city'] = 'Beverly Hills'
        tOrder['address_country'] = 'United States'
        tOrder['address_country_code'] = 'US'
        tOrder['address_name'] = 'Test Address'
        tOrder['address_state'] = 'California'
        tOrder['address_street'] = '9876 Wilshire Boulevard'
        tOrder['address_zip'] = '90210'
        tOrder['notify_version'] = '3.4'
        
        #logging.debug(str(tOrder))
        
        tAvailableEligibility = ["Ineligible","Partially Eligible - INR Only","Eligible"]
        tOrder['protection_eligibility'] = random.choice(tAvailableEligibility)
        
        tAvailableStatus = ["verified","unverified"]
        tOrder['payer_status'] = random.choice(tAvailableStatus)
        
        if(tType == "random" or tType == "me"):                    
            tOrder['mc_gross'] = tRandomPrice
            tOrder['payment_gross'] = tRandomPrice
            tOrder['txn_type'] = 'web_accept'
            tOrder['discount'] = '0.0'
            tOrder['handling_amount'] = '0.0'
            tOrder['insurance_amount'] = '0.0'
            tOrder['item_number'] = '1'
            tOrder['mc_fee'] = '0.0'
            tOrder['COUNTRYCODE'] = 'US'
            tOrder['address_country'] = 'United States'
            tOrder['payment_fee'] = '0.0'
            tOrder['quantity'] = "1"
            tOrder['shipping'] = "0.0"
            tOrder['shipping_discount'] = "0.0"
            tOrder['shipping_method'] = "Default"
            tOrder['tax'] = "0.0"
            
            tOrder['item_name'] = tRandomAmount.upper() + "Transfer Code"
            
            tReferralCodes = ["", "69a8e184"]
            tRandomReferral = random.choice(tReferralCodes)
            
            tPromoCodes = ["SMELITE10"]
            tRandomPromoCode = random.choice(tPromoCodes)   
            
            tOrder['option_name1'] = 'Test Order Name'      #name    
            tOrder['option_name4'] = 'RS Test Name'         #rs name 
            tOrder['option_name5'] = tRandomReferral        #referral
            tOrder['option_name5'] = tRandomPromoCode       #promocode formerly option 6
            tOrder['option_name7'] = tRandomAmount          #gold amount
            
        #logging.debug(str(tOrder))
        if(tType == "random" or tType == "viprandom"):
            tRandomEmail = 'sm-test-email-' + "".join(tRandomNumberList) + "@smokinmils.com"
            tOrder['payer_email'] = tRandomEmail
            tOrder['payer_id'] = "".join(tRandomNumberList) + "-testid"
            tOrder['txn_id'] = "".join(tRandomNumberList)        
            tOrder['custom'] = '65.91.31.0'
            tOrder['option_name2'] = tRandomEmail           #email
            tOrder['option_name3'] = '310-274-7777'         #number
            tOrder['transaction_subject'] = '65.91.31.0'
        #logging.debug(str(tOrder))
        if(tType == "me" or tType == "vipme"):
            tOrder['custom'] = '75.138.80.254'
            tOrder['payer_email'] = 'kenneth.posey@gmail.com'
            tOrder['payer_id'] = 'FE6TJMYCTZ9CA'
            tOrder['txn_id'] = "".join(tRandomNumberList)        
            tOrder['option_name2'] = 'kenneth.posey@gmail.com'
            tOrder['option_name3'] = '678-499-6457'   
            tOrder['transaction_subject'] = '75.138.80.254'
        #logging.debug(str(tOrder))
        if(tType == "viprandom" or tType == "vipme"):
            tOrder['payment_gross'] = "8.99"
            tOrder['transaction_subject'] = "VIP Membership"
            tOrder['item_name'] = "VIP Membership"
            tOrder['item_number'] = "VIP"
            tOrder['mc_gross'] = "8.99"
            tOrder['txn_type'] = "subscr_payment"
            tOrder['subscr_id'] = "".join(tRandomNumberList)
        #logging.debug(str(tOrder))
        tOrder['payment_status'] = 'Completed'
        tOrder['payment_type'] = 'Instant'
        tOrder['last_name'] = "Pleco"
        tOrder['first_name'] = "Kort"
        
        tOrder['fake'] = 'True'        
        #logging.debug("Last call: " + str(tOrder))
        tPayloadEncoded = urllib.urlencode(tOrder)

        #logging.debug("Encoded: " + str(tPayloadEncoded))

        tUrl = "http://smokin-goldshop.appspot.com/paypalipn"
        #logging.debug("Url: " + str(tUrl))
        
        request_cookies = mechanize.CookieJar()
        request_opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(request_cookies))
        request_opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
        
        mechanize.install_opener(request_opener)
        tResponse = mechanize.urlopen(url = tUrl, timeout = 25.0, data = tPayloadEncoded)
        
        
        tOrderQuery = Order().all()
        tOrderQuery.filter("orderIsGenerated", True)
        tOrderQuery.order("-orderCreated")
        tOrderList = tOrderQuery.fetch(limit=30)
        
        tContext['orders'] = tOrderList        
        
        #logging.debug("Response: " + str(tResponse))
        return tContext
    