
import os
    
from google.appengine.api import memcache, users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from base import BaseHandler

class LostHandler(BaseHandler):
    LOCATION = "../views/404.html"
    def GetContext(self):
        return {}