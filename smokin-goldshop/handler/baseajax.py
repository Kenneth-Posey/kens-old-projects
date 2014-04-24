from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
import locale, os, logging

class BaseAjax(webapp.RequestHandler):
    REDIRECT = False
    
    def GetContext(self):
        return {}
    def PostContext(self):
        return {}
    def GetLocation(self):
        return self.LOCATION
    def GetUser(self):
        return users.get_current_user()
    def IsUserAdmin(self):
        return users.is_current_user_admin()
    def GetRedirect(self):
        return self.REDIRECT
        
    def post(self):
        tUser = self.GetUser()
        locale.setlocale(locale.LC_ALL, "")
        tResponse = {}
        tResponse['tResponseText'] = "Empty Response"
        
        if (tUser == None):
            self.response.out.write("User Not Authorized")
            return ""
        else:
            self.USER = tUser
            tResponse.update(self.PostContext())
            self.response.out.write(str(tResponse['tResponseText']))
