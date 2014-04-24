
import os, urllib, logging, datetime
    
from google.appengine.api import memcache, users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from models.ipinfo import IpInfo
from models.order import Order
from models.customer import Customer
from base import BaseHandler

class CustomerHandler(BaseHandler):
    LOCATION = "../views/customer.html"
    def GetContext(self):
        
        tUser = self.GetUser()        
        tCustomerList = []
        tCustomerOrders = []
        tCustomerOrderKeys = []
        tOrderData = {}
        tOrder = Order()
        tShowSearch = False
        tCustomerLookup = CustomerHandler()
        tCustomerKey = urllib.unquote(self.request.get('key'))
        
        if(tCustomerKey):
            tCustomerList.append(tCustomerLookup.GetCustomerByKey(tCustomerKey))
        #logging.debug(str(len(tCustomerList)))
        
        if (tCustomerList == None or len(tCustomerList) == 0):
            tShowSearch = True
        else:
            tShowSearch = False
            tCustomer = Customer()
            tCustomer = tCustomerList[0]
            
            #Get date 30 days ago
            tStartDate = datetime.datetime.now()
            tIncrement = datetime.timedelta(days = -30)
            tEndDate = tStartDate + tIncrement
            tCustomerOrderQuery = Order.all()
            tCustomerOrderQuery.filter("orderCreated >", tEndDate)
            tCustomerOrderQuery.filter("orderCustomer", tCustomerKey)
            tCustomerOrderQuery.filter("orderDeliver", 'True')
            tCustomerOrders = tCustomerOrderQuery.fetch(1000)
            #logging.debug("30 day date: " + str(tEndDate))
            #logging.debug("30 day orders: " + str(len(tCustomerOrders)))
            tCustomerOrderTotal = 0.0
            for tCustomerOrder in tCustomerOrders:
                tCustomerOrderTotal += float(tCustomerOrder.orderCost)
            if (tOrder.orderDeliver == 'False'):
                tCustomerOrderTotal += tCurrentCost
            tOrderData['orderTotal'] = str("%.2f"% tCustomerOrderTotal)
            
            #Get date 24 hours ago
            tStartDate = datetime.datetime.now()
            tIncrement = datetime.timedelta(days = -1)
            tEndDate = tStartDate + tIncrement
            tCustomerOrderQuery = Order.all().filter("orderCreated >", tEndDate)
            tCustomerOrderQuery.filter("orderCustomer", tCustomerKey)
            tCustomerOrderQuery.filter("orderDeliver", 'True')
            tCustomerOrders = tCustomerOrderQuery.fetch(1000)
            #logging.debug("24 hour date: " + str(tEndDate))
            #logging.debug("24 hour orders: " + str(len(tCustomerOrders)))
            tCustomerOrderTotal24 = 0.0
            for tCustomerOrder in tCustomerOrders:
                tCustomerOrderTotal24 += float(tCustomerOrder.orderCost)
                
            if (tOrder.orderDeliver == 'False'):
                tCustomerOrderTotal24 += tCurrentCost
            tOrderData['orderTotal24'] = str("%.2f" % tCustomerOrderTotal24)
            
            #Get date 15 days ago
            #tStartDate = datetime.datetime.now()
            #tIncrement = datetime.timedelta(days = -15)
            #tEndDate = tStartDate + tIncrement
            #tCustomerOrderQuery = Order.all().filter("orderCreated >", tEndDate)
            #tCustomerOrderQuery.filter("orderCustomer", tCustomerKey)
            #tCustomerOrderQuery.filter("orderDeliver", 'True')
            #tCustomerOrders = tCustomerOrderQuery.fetch(1000)
            #logging.debug("15 day date: " + str(tEndDate))
            #logging.debug("15 day orders: " + str(len(tCustomerOrders)))
            #tCustomerOrderTotal15 = 0.0
            #for tCustomerOrder in tCustomerOrders:
                #tCustomerOrderTotal15 += float(tCustomerOrder.orderCost)
                
            #if (tOrder.orderDeliver == 'False'):
                #tCustomerOrderTotal15 += tCurrentCost
            #tOrderData['orderTotal15'] = str("%.2f" % tCustomerOrderTotal15)
            
            #logging.debug(str(tCustomerKey))
            tOrderQuery = Order.all()
            tOrderQuery.filter("orderCustomer", tCustomerKey)
            tOrderQuery.order("-orderCreated")
            tCustomerOrders = tOrderQuery.fetch(20)
            #logging.debug(str(tCustomerOrders))
            
                
        tShowSearch = str(tShowSearch)
        
        return {
            'result':    tCustomerList,
            'customerorders': tCustomerOrders,
            'tOrderData':tOrderData,
            'search':    tShowSearch,
        }   
        
    def PostContext(self):
        tCustomerKey = ""
        tCustomer = Customer()
        tCustomerLookup = CustomerHandler()
        
        tAction = str(self.request.get('action')).lower()
        tCustomerKey = str(self.request.get('key'))
        tItem = str(self.request.get('item')).lower()
        
        if (tAction != None and len(tAction) > 0 and tAction == "search"):
            tSearchEmail = str(urllib.unquote(self.request.get('email'))).lower()
            tSearchPpid = str(urllib.unquote(self.request.get('ppid')))
            if (tSearchEmail != None and len(tSearchEmail) > 0):
                tCustomerList = tCustomerLookup.GetCustomerByEmail(tSearchEmail)
            elif (tSearchPpid != None and len(tSearchPpid) > 0):
                tCustomerList = tCustomerLookup.GetCustomerByPpid(tSearchPpid)
            tCustomer = tCustomerList[0]
        elif (tCustomerKey != None and len(tCustomerKey) > 0):
            tCustomer = Customer().get(tCustomerKey)
            if (tAction == 'phone'):
                tCustomer.customerPhone = tItem
                #logging.debug("Number saving success: " + tItem)
            if (tAction == 'idverified'):
                tCustomer.customerIdVerified = True
                #logging.debug("Customer Id Verified")
            if (tAction == 'idverify'):
                tCustomer.customerIdLink = tItem
                #logging.debug("Customer Id: " + tItem)
            if (tAction == 'memo'):
                tCustomer.customerMemo = tItem
                #logging.debug("Customer Memo: " + tItem)
            tCustomer.put()
        if(tCustomer):
            tCustomerKey = str(tCustomer.key())
        
        self.LOCATION = '/customerlookup?key=' + str(tCustomerKey)
        self.REDIRECT = True
        return {} #need to return something for processing
        #self.redirect(tLocation)
        
        
    def GetCustomerByEmail(self, pEmail):
        #logging.debug("Searching for: " + pEmail)
        tCustomerResults = []
        tCustomerQuery = Customer().all()
        tCustomerQuery.filter('customerEmail', pEmail)
        tCustomerResults = tCustomerQuery.fetch(10)
        #logging.debug("Found these results: " + str(len(tCustomerResults)))
        return tCustomerResults
    
    def GetCustomerByName(self, pName):
        #logging.debug("Searching for: " + pName)
        tCustomerResults = []
        tCustomerQuery = Customer().all()
        tCustomerQuery.filter('customerLastName', pName)
        tCustomerResults = tCustomerQuery.fetch(10)
        #logging.debug("Found these results: " + str(len(tCustomerResults)))
        return tCustomerResults
    
    def GetCustomerByPpid(self, pPpid):
        #logging.debug("Searching for: " + pPpid)
        tCustomerResults = []
        tCustomerQuery = Customer().all()
        tCustomerQuery.filter('customerPaypalId', pPpid)
        tCustomerResults = tCustomerQuery.fetch(10)
        #logging.debug("Found these results: " + str(len(tCustomerResults)))
        return tCustomerResults
    
    def GetCustomerByKey(self, pKey):
        tCustomer = Customer.get(pKey)
        return tCustomer
    
    def GlobalBlacklistCustomer(self, pKey):
        tCustomer = Customer()
        tCustomerHandler = CustomerHandler()
        #logging.debug("Global Blacklisting Customer: " + str(pKey))
        try:
            tCustomer = tCustomerHandler.GetCustomerByKey(pKey)
            tCustomer.customerIsGlobalBlacklisted = True
            tCustomer.put()
            
            tIpList = tCustomer.customerIpAddresses
            #logging.debug("Customer IPs: " + str(tIpList))
            tUniqueIps = set(tIpList)
            tUniqueIps = list(tUniqueIps)
            ip = IpInfo()
            for tIp in tUniqueIps:
                #logging.debug("Blacklisting IP: " + str(tIp))
                tIps = IpInfo().all()
                tIps.filter("ip", tIp)
                tIpModels = tIps.fetch(100)
                for ip in tIpModels:
                    ip.ipIsGlobalBlacklisted = True
                    ip.put()
            return True
        except:
            return False
        
    def PaBlacklistCustomer(self, pKey):
        #logging.debug("PA Blacklisting Customer: " + str(pKey))
        tCustomer = Customer()
        tCustomerHandler = CustomerHandler()
        try:
            tCustomer = tCustomerHandler.GetCustomerByKey(pKey)
            tCustomer.customerIsPaBlacklisted = True
            tCustomer.put()
            
            tIpList = tCustomer.customerIpAddresses
            #logging.debug("Customer IPs: " + str(tIpList))
            tUniqueIps = set(tIpList)
            tUniqueIps = list(tUniqueIps)
            ip = IpInfo()
            for tIp in tUniqueIps:
                #logging.debug("Blacklisting IP: " + str(tIp))
                tIps = IpInfo().all()
                tIps.filter("ip", tIp)
                tIpModels = tIps.fetch(100)
                for ip in tIpModels:
                    ip.ipIsPaBlacklisted = True
                    ip.put()
            return True
        except:
            return False
        
        
        
        
        
        
        
        
        
        