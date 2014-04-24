from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from protorpc import messages
from protorpc import remote
from protorpc.webapp import service_handlers

from handler.orderajax import BlacklistAjax
from handler.orderajax import OrderAjax

service_mappings = service_handlers.service_mapping(
    [('/orderajax', OrderAjax),
     ('/blacklist', BlacklistAjax)
    ])

application = webapp.WSGIApplication(service_mappings)

def main():
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()