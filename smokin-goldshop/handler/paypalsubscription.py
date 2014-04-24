
import os, re, math, urllib, logging, datetime, time
from public import mechanize    
from google.appengine.api import memcache, users, urlfetch, taskqueue, mail
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import Request, RequestHandler
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

class PaypalSubscriptionHandler(webapp.RequestHandler):
    LOCATION = '../views/paypalsubscriptions.html'
    def GetContext(self):
        tContext = {}
        
        
        return tContext