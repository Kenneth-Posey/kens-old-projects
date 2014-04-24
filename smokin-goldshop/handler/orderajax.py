
import logging
from google.appengine.ext import webapp
#from google.appengine.ext.webapp import util
from protorpc import util

from protorpc import messages
from protorpc import remote
from protorpc import service_handlers
from protorpc.service_handlers import ServiceHandlerFactory

from customerhandler import CustomerHandler
from models.customer import Customer

class OrderRequest(messages.Message):
    request = messages.StringField(1, required = True)
    
class OrderResponse(messages.Message):
    response = messages.StringField(1, required = True)
    
class OrderAjax(remote.Service):
    @remote.method(OrderRequest, OrderResponse)
    def ajax(self, request):
        #logging.debug("test hit")
        
        tRequest = self.request
        tArguments = tRequest.arguments()
        
        tArgumentDic = {}
        
        for tArgument in tArguments:
            tArgumentDic[tArgument] = tRequest.get(tArgument)
            
        #logging.debug("==========Beginning Request==========")
        
        for tArgKey in tArgumentDic.keys():
            logging.debug("Paypal Post Key: " + str(tArgKey) + " with Value: " + str(tArgumentDic[tArgKey]))
            
        #logging.debug("==========Stored Request==========")
        return OrderResponse(response = "Request Received")
    
class BlacklistRequest(messages.Message):
    BlackListType = messages.StringField(1, required = True)
    Customer = messages.StringField(2, required = True)

class BlacklistResponse(messages.Message):
    Response = messages.StringField(1, required = True)
    
class BlacklistAjax(remote.Service):
    @remote.method(BlacklistRequest, BlacklistResponse)
    def ajax(self, request):
        #logging.debug("starting")
        tRequest = request
        #logging.debug(str(tRequest))
        tArgumentDic = {}
        tCustomerHandler = CustomerHandler()
        tCustomer = Customer()
        #logging.debug("Beginning Blacklist of type " + tRequest.BlackListType + " for customer " + tRequest.Customer)
        
        if(tRequest.BlackListType == 'PA'):
            tCustomerHandler.PaBlacklistCustomer(tRequest.Customer)
            #logging.debug("Blacklisted PA")
            return BlacklistResponse(Response = "PA Blacklisted!")
        elif(tRequest.BlackListType == 'Global'):
            tCustomerHandler.GlobalBlacklistCustomer(tRequest.Customer)
            #logging.debug("Blacklisted Global")
            return BlacklistResponse(Response = "Global Blacklisted!")
        else:
            #logging.debug("Error Blacklisting")
            return BlacklistResponse(Response = "Error Blacklisting")
    
    

service_mappings = service_handlers.service_mapping(
    [('/orderajax', OrderAjax),
     ('/blacklist', BlacklistAjax)
    ])

application = webapp.WSGIApplication(service_mappings, debug=True)

def main():
    #util.run_wsgi_app(application)
    service_handlers.run_services(service_mappings)

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    