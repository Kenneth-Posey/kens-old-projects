
import os, logging, re, cgi, urllib
from public import mechanize    
from google.appengine.api import memcache, users, urlfetch, taskqueue
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from models.paypalipn import PaypalIPN
from base import BaseHandler

class PaypalIpnHistory(BaseHandler):
    LOCATION = "../views/paypalipn.html"
    def GetContext(self):
        tContext = {}
        
        tActionDic = {}
        tActionDic['signup'] = 'subscr_signup'
        tActionDic['payment'] = 'subscr_payment'
        tActionDic['cancel'] = 'subscr_cancel'
        tActionDic['fail'] = 'subscr_failed'
        
        tIpnList = []
        tPaypalIpn = PaypalIPN().all()
        
        #variable filter
        tAction = str(self.request.get("action"))
        if(tAction in tActionDic.keys()):
            tPaypalIpn.filter('txn_type', tActionDic[tAction])
        
        tPaypalIpn.order('-ipnMessageSent')
        tIpnList = tPaypalIpn.fetch(limit=150)    
        
        tContext['ipnlist'] = tIpnList
        
        return tContext