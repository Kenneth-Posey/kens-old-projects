
import os, re, math, urllib, logging, datetime
import time, uuid
from public import mechanize
from customerhandler import CustomerHandler

from models.customer import Customer
from google.appengine.api import memcache, users, mail
from google.appengine.ext import webapp
from models.referrer import Referrer
from base import BaseHandler
    
class Referral(webapp.RequestHandler):
    def get(self):
        tReferrer = Referrer()
        tEmail = ""
        tEmail = str(urllib.unquote(self.request.get('email'))).lower()
        tReferrerQuery = Referrer.all()
        tReferrerQuery.filter('referEmail', tEmail)
        #logging.debug("Email Received: " + tEmail)
        try:
            tReferrer = tReferrerQuery.fetch(1)[0]
        except:
            tReferrer.referEmail = tEmail
            tReferrer.referGp = 28000000.0
            tReferrer.referCash = 20.0
            tReferrer.referSimpleCash = "$20.00"
            tReferrer.referSimpleGold = "28m"
            
            tBaseUuid = str(uuid.uuid4())
            tSplitUuid = tBaseUuid.split('-')
            tReferrer.referId = tSplitUuid[0]
            tReferrer.referPin = tSplitUuid[1]
            tReferrer.put()
            
        tMessage = """                    Dear """ + str(tEmail) + """

Your referral ID, link, and PIN are shown below.

Referral ID: """ + str(tReferrer.referId) + """
PIN: """ + str(tReferrer.referPin) + """
Referral link: http://www.smokinmils.com/goldshop.php?referral_id=""" + tReferrer.referId + """

Please note that you will need your referral ID and your PIN to check your balance or collect payments in the future, so don't lose them!

To start earning money you need people to visit your referral ID link and make purchases. You get 20% of the cash or gold amount on a first purchase and 10% for repeat purchases. You can post your referral link anywhere, such as in discussions on Runescape related forums. Your balance will increase any time someone makes a purchase using your link. You are likely to get clicks if you talk about a good experience buying gold from us. You could also put the link in your forum signature.

You can put an image banner in a forum signature by inserting this code:

[url=http://www.smokinmils.com/goldshop.php?referral_id=""" + tReferrer.referId + """][img]http://i49.servimg.com/u/f49/14/29/83/59/goldsh10.jpg[/img][/url]

You can add a hyperlink that says "Smokin Mils Gold Shop" by inserting this code:

[url=http://www.smokinmils.com/goldshop.php?referral_id=""" + tReferrer.referId + """]Smokin Mils Gold Shop[/url]

Your current balance is """ + str(tReferrer.referSimpleCash) + """ USD or """ + str(tReferrer.referSimpleGold) + """ gold. To request a payout please speak to an agent in the live chat on our website. Please note that the minimum payout is $100 USD or 130M gold.

To check your current balance in the future please visit http://smokinmils.com/referrals.php and fill in the form on the right.

Kind regards,
Smokin Mils Staff
http://smokinmils.com/goldshop.php"""
        #raise Exception ("not implemented")
        #logging.debug("Referral Email Sent to " + str(tEmail))
        mail.send_mail(sender = "Smokin Mils Goldshop <Support@eMeMO.com>",
                       to = tEmail,
                       subject = "Smokin Mils Goldshop Referral Program Information",
                       body = tMessage)
        

class ReferralBalance(BaseHandler):
    LOCATION = "../views/referral.html"
    def GetContext(self):
        tContext = {}
        tContext['search'] = "True"
        tContext['error'] = "Enter the referrer id you wish to look up"
        return tContext
        
    def PostContext(self):
        tContext = {}
        tReferrer = Referrer()
        tRefBalance = ReferralBalance()
        tReferralId = str(urllib.unquote(self.request.get('id')).strip())
        tPaid = str(urllib.unquote(self.request.get('key')).strip())     
        tReferQuery = Referrer.all()
        tReferQuery.filter('referId', tReferralId)
        
        #logging.debug("Referrer id: " + tReferralId)
        #logging.debug("Pay: " + tPaid)
        
        #try:
        tContext['search'] = "False"
        
        if(len(tPaid) > 0):
            tRefBalance.PayReferrer(tPaid)
            tContext['error'] = 'Referrer Paid Successfully'
            
        tReferrer = tReferQuery.fetch(1)[0]
        
        tContext['referrer'] = tReferrer
        return tContext
                
    @staticmethod
    def PayReferrer(pKey):
        tReferrerKey = str(pKey)
        tReferrer = Referrer()
        tReferrer = Referrer.get(str(tReferrerKey))
        
        tReferrer.referCash = 0.0
        tReferrer.referGp = 0.0
        tReferrer.referSimpleCash = '$0.00'
        tReferrer.referSimpleGold = '0m'
        tReferrer.put()
        #logging.debug("Referrer Paid: " + str(tReferrerKey))
        
        
class CalcReferral(webapp.RequestHandler):
    def post(self):
        from models.order import Order
        from _numbertogp import NumberToGp
        tCalc = CalcReferral()
        tOrderKey = self.request.get('key')
        tOrder = Order()
        tOrder = Order.get(str(tOrderKey))
        
        tReferCode = tOrder.orderReferralCode
        
        if (tReferCode == None):
            tReferCode = ""
        
        #logging.debug("Referrer Code: " + tReferCode)
        
        if (tReferCode == "" or tReferCode == None):
            return None
        
        tRefererQuery = Referrer.all()
        tRefererQuery.filter('referId', tReferCode)
        tReferer = Referrer()
        try:
            tReferer = tRefererQuery.fetch(1)[0]
        except:
            #logging.debug("Referrer Code Not Found: " + tReferCode)
            return None
        
        tGp = 0.0
        tCash = 0.0
        
        #No matching referrers and paypal emails
        if(tReferer.referEmail != None):
            if(str(tReferer.referEmail).lower() == str(tOrder.orderPaypalEmail).lower()):
                return None
        
        if (tReferer.referGp == 0.0 or tReferer.referCash == 0.0):
            tGp = tOrder.orderQuantity * 0.2
            tCash = tOrder.orderCost * 0.2
        else:
            tGp = float(tReferer.referGp) + (tOrder.orderQuantity * 0.1)
            tCash = float(tReferer.referCash) + (tOrder.orderCost * 0.1)
        
        tReferer.referGp = tGp
        tReferer.referCash = tCash
        tReferer.referSimpleGold = NumberToGp.ConvertIntToBet(int(float(tGp)))
        tReferer.referSimpleCash = tCalc.FormatCurrency(tCash)
        
        #logging.debug("Referrer Gp: " + str(tGp))
        #logging.debug("Referrer Cash: " + str(tCash))
        #logging.debug("Referrer Simple Gold: " + str(tReferer.referSimpleGold))
        #logging.debug("Referrer Simple Cash: " + str(tReferer.referSimpleCash))
        
        tReferer.put()
        
    def FormatCurrency(self, pCash):
        tCash = ""
        tCash = str(pCash)
        tCashDollars = tCash.split('.')[0]
        tCashCents = tCash.split('.')[1]
        tCashCentsRounded = tCashCents[0:2]
        if (len(tCashCentsRounded) == 0):
            tCashCentsRounded = tCashCentsRounded + "00"
        elif(len(tCashCentsRounded) == 1):
            tCashCentsRounded = tCashCentsRounded + "0"
        
        return "$" + tCashDollars + "." + tCashCentsRounded
            
class AddReferralBonus(webapp.RequestHandler):
    def get(self):
        tRefQuery = Referrer.all()
        tReferrer = Referrer()
        tRefQuery.filter("referCash =", 0.0)
        
        tReferrers = tRefQuery.fetch(200)
        
        try:
            for tReferrer in tReferrers:
                tReferrer.referCash = 20.0
                tReferrer.referGp = 28000000.0
                tReferrer.referSimpleCash = '$20.00'
                tReferrer.referSimpleGold = '28m'
                tReferrer.put()
            self.response.out.write('Success')
        except: 
            self.response.out.write('Failure')
            
        