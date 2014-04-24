import webapp2

from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
import locale, os, logging, datetime

from models.agent import Agent


class BaseHandler(webapp2.RequestHandler):
    REDIRECT = False
    GOLDTYPE = ''
    REQUIRE_AUTH_POST = True
    REQUIRE_AUTH_GET = True
    
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
        
    def get(self):
        tUser = self.GetUser()
        locale.setlocale(locale.LC_ALL, "")
        tContext = {}
        tContext['login'] = users.create_login_url(self.request.uri)
        tContext['logout'] = users.create_logout_url(self.request.uri)
        tContext['error'] = ''
        tContext['TIME'] = str(datetime.datetime.now())
        
        if (tUser == None):
            if (self.GetLocation() != "../views/index.html"):
                self.redirect("/")
            else:
                tContext['error'] = 'Login is required to access the portal'
                tTemplate = os.path.join(os.path.dirname(__file__), "../views/index.html")
                self.response.out.write(render(tTemplate, tContext))
            return
        else:
            self.USER = tUser
            tContext['user'] = tUser
            tContext.update(self.GetContext())
            tLocation = self.GetLocation()
            tRedirect = self.GetRedirect()
            
            #logging.debug("User: " + str(tUser.email()))
            #logging.debug("Context: " + str(tContext))
            #logging.debug("Location: " + str(tLocation))
            #logging.debug("Redirect: " + str(tRedirect))
              
            #if(tContext.has_key('agent')):
            #    tAgent = tContext['agent']
            #else:
            try:
                tAgent = Agent().GetAgentByEmail(str(tUser.email()))
            except:
                tAgent = Agent()          
                    
            if(tAgent.agentSoundDelay == None or tAgent.agentSoundDelay == ""):
                tAgent.agentSoundDelay = 10000
                
            if(tAgent.agentSoundSelection == None or tAgent.agentSoundSelection == ""):
                tAgent.agentSoundSelection = "beep"
            
            if(tAgent.agentSoundRepeat == None or tAgent.agentSoundRepeat == ""):
                tAgent.agentSoundRepeat = 1
                        
            #logging.debug("Sound delay: " + str(tAgent.agentSoundDelay))
            #logging.debug("Sound selection: " + str(tAgent.agentSoundSelection))
            #logging.debug("Sound repeat: " + str(tAgent.agentSoundRepeat))            
            tContext['agent'] = tAgent
            
            logging.debug('Context: ' + str(tContext))
            
            if tAgent.agentIsAdmin:
                tContext['isAdmin'] = 'True'
            
            if(tAgent.agentIsEnabled == False):
                tContext['error'] = 'Your agent access is not active'
                tTemplate = os.path.join(os.path.dirname(__file__), "../views/index.html")
                self.response.out.write(render(tTemplate, tContext))
                return
            
            if(tRedirect == False):
                tTemplate = os.path.join(os.path.dirname(__file__), tLocation)
                self.response.out.write(render(tTemplate, tContext))
            else:
                self.redirect(tLocation)
            
    def post(self):
        tUser = self.GetUser()
        locale.setlocale(locale.LC_ALL, "")
        tContext = {}
        tContext['login'] = users.create_login_url(self.request.uri)
        tContext['logout'] = users.create_logout_url(self.request.uri)
        tContext['error'] = ''
        tContext['TIME'] = str(datetime.datetime.now())
        
        if (tUser == None and self.REQUIRE_AUTH_POST == True):
            if (self.GetLocation() != "../views/index.html"):
                self.redirect("/")
            else:
                tTemplate = os.path.join(os.path.dirname(__file__), "../views/index.html")
                self.response.out.write(render(tTemplate, tContext))
            return
        else:
            self.USER = tUser
            tContext['user'] = tUser
            tPostContext = self.PostContext()
            
            tContext.update(tPostContext)
            tLocation = self.GetLocation()
            tRedirect = self.GetRedirect()
            
            #logging.debug("User:" + str(tUser.email))
            #logging.debug("Context: " + str(tContext))
            #logging.debug("Location: " + str(tLocation))
            #logging.debug("Redirect: " + str(tRedirect))

            #if(tContext.has_key('agent')):
                #tAgent = tContext['agent']
            #else:
            try:
                tAgent = Agent().GetAgentByEmail(str(tUser.email()))
            except:
                tAgent = Agent()          
                    
            if(tAgent.agentSoundDelay == None or tAgent.agentSoundDelay == ""):
                tAgent.agentSoundDelay = 10000
                
            if(tAgent.agentSoundSelection == None or tAgent.agentSoundSelection == ""):
                tAgent.agentSoundSelection = "beep"
            
            if(tAgent.agentSoundRepeat == None or tAgent.agentSoundRepeat == ""):
                tAgent.agentSoundRepeat = 1
                        
            #logging.debug("Sound delay: " + str(tAgent.agentSoundDelay))
            #logging.debug("Sound selection: " + str(tAgent.agentSoundSelection))
            #logging.debug("Sound repeat: " + str(tAgent.agentSoundRepeat))            
            tContext['agent'] = tAgent            
            
            if(tContext.has_key('nowrite')):
                if(tContext['nowrite'] == True):
                    return
            else:
                if(tRedirect == False):
                    tTemplate = os.path.join(os.path.dirname(__file__), tLocation)
                    self.response.out.write(render(tTemplate, tContext))
                else:
                    self.redirect(tLocation)
