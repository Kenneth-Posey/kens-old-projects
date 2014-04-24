
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app

from handler.paorderhandler import PaOrderHandler

tMailHandlerList = []

tMailHandlerList.append(
    PaOrderHandler.mapping()
    )

tMailApplication = webapp.WSGIApplication(tMailHandlerList, debug=True)

def mail():
    run_wsgi_app(tMailApplication)

if __name__ == '__main__':
    mail()