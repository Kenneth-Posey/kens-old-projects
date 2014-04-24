
import os, logging
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from handler.iplookup import IpLookup
from models.customer import Customer


class CustomerEmailReset(webapp.RequestHandler):
    def get(self):
        tCQ = Customer().all()
        tList = tCQ.fetch(5000)
        #logging.debug("Updating: " + str(len(tList)))
        cust = Customer()
        for cust in tList:
            cust.customerEmail = str(cust.customerEmail).lower()
            cust.put()
        self.response.out.write("DONE")
        
class BlankKiller(webapp.RequestHandler):
    def get(self):
        tCQ = Customer().all()
        tCQ.filter('customerPaypalId', 'NULL')
        tCQ = db.GqlQuery("SELECT * FROM Customer where customerPaypalId = NULL")
        tList = tCQ.fetch(500)
        #logging.debug("Updating: " + str(len(tList)))
        cust = Customer()
        for cust in tList:
            cust.delete()
        self.response.out.write("DONE")
        
class OrderPageAjax(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        context = {
            'user':      user,
            'login':     users.create_login_url(self.request.uri),
            'logout':    users.create_logout_url(self.request.uri),
        }
        tmpl = os.path.join(os.path.dirname(__file__), 'orderpageajax.html')
        self.response.out.write(render(tmpl, context))
        
        
class PaypalWipe(webapp.RequestHandler):
    def post(self):
        tOrderQuery = db.GqlQuery("Select * From Order")
        tOrderList = tOrderQuery.fetch(1)
        if (tOrderList[0]):
            tOrder = tOrderList[0]
            #logging.debug("Deleting Item: " + str(tOrder))
            tOrder.delete()
            taskqueue.add(url = '/resetorders', params = {})
    def get(self):
        tOrderQuery = db.GqlQuery("Select * From Order")
        tOrderList = tOrderQuery.fetch(1)
        if (tOrderList[0]):
            tOrder = tOrderList[0]
            #logging.debug("Deleting Item: " + str(tOrder))
            tOrder.delete()
            taskqueue.add(url = '/resetorders', params = {})

class PaypalMonitor(webapp.RequestHandler):
    
    #Modified for account security
    API_PASSWORD  = "REDACTED"
    API_USERNAME  = "REDACTED"
    API_SIGNATURE = "REDACTED"
    
    def get(self):
        tUrl = "https://api-3t.paypal.com/nvp"
        tOperation = "TransactionSearch"
        tPaypal = PaypalTrigger()
        tDateSearch = CurrentTimestamp()
        tOrderList = []
        tPaypalPayload = {}        
        tPayload = {}
        tTimestampQueryString = "Select * from CurrentTimestamp"
        tTimestampQuery = db.GqlQuery(tTimestampQueryString)
        tStartDate = tTimestampQuery.fetch(1)[0]
        
        
            