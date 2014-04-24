
import os, logging, re, cgi, urllib
from public import mechanize    
from google.appengine.api import memcache, users, urlfetch, taskqueue
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from models.paypalipn import PaypalIPN
from base import BaseHandler

class PaypalIpnDump(BaseHandler):
    LOCATION = "../views/paypalipndump.html"
    def GetContext(self):
        tContext = {}
        tResultDictionary = {}
        
        tIpnDump = urllib.unquote(self.request.get('key'))
        if(tIpnDump != None and len(tIpnDump) > 0):
            tIpnDump = PaypalIPN.get(tIpnDump)
        
        tResultSplit = tIpnDump.ipnRawMessage.split('&')
        
        for tPair in tResultSplit:
            tSplitPair = tPair.split("=")
            try:
                tResultDictionary[tSplitPair[0]] = tSplitPair[1]
                #logging.debug(tSplitPair[0] + "    " + tSplitPair[1])
            except:
                logging.error("Error splitting item: " + str(tPair))        
        
        tDump = str(tIpnDump.ipnRawMessage).replace("&", " ")
        
        tContext['data'] = tIpnDump.__dict__['_dynamic_properties']
        tContext['dump'] = tDump
        
        return tContext