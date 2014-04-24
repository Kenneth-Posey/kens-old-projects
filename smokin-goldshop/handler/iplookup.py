
import os, logging, re, cgi, urllib
from public import mechanize    
from google.appengine.api import memcache, users, urlfetch, taskqueue
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
from models.ipinfo import IpInfo
from models.order import Order
from base import BaseHandler

class IpLookup(BaseHandler):
    LOCATION = "../views/iplookup.html"
    def GetContext(self):
        return {}
        
    def post(self):
        tIpLookup = IpLookup()
        tIpStore = IpInfo()
        tIp = str(self.request.get('ip'))
        tTransactionId = str(self.request.get('transid'))
        
        tIpInfo = {}
        #logging.debug("Scraping Ip: " + tIp)
        
        if (tIp != None and len(tIp) > 0):
            tIpInfo = tIpLookup.IpInfoScraper(tIp)
        else:
            tIpInfo = {}
            tIpInfo['country'] = ""
            tIpInfo['host'] = ""
            tIpInfo['state'] = ""
            tIpInfo['isp'] = ""
            tIpInfo['proxy'] = ""
            tIpInfo['type'] = ""
        
        tIpStore.ip = tIp
        tIpStore.ipCountry = tIpInfo['country']
        tIpStore.ipHost = tIpInfo['host']
        tIpStore.ipState = tIpInfo['state']
        tIpStore.ipIsp = tIpInfo['isp']
        tIpStore.ipProxy = tIpInfo['proxy']
        tIpStore.ipType = tIpInfo['type']
        tIpStore.ipOrder = tTransactionId
        tIpKey = tIpStore.put()
        
        #logging.debug("Stored IP: " + tIp + " at Key " + str(tIpKey))
        
        tOrder = Order()
        tOrderQuery = Order().all()
        #logging.debug("Transaction Id: " + tTransactionId)
        tOrderQuery.filter("orderTransactionId", tTransactionId)
        tOrder = tOrderQuery.fetch(1)[0]
        
        tMobilePhone = tOrder.orderMobileNumber
        tCustomerKey = tOrder.orderCustomer
        tOrderKey = str(tOrder.key())
        #logging.debug("IP Address Mobile Number " + str(tMobilePhone))
        if (tMobilePhone != None and len(tMobilePhone) > 0):
            taskqueue.add(url="/phonelookup", countdown = 1, params = { "order": tOrderKey, 
                                                                        "customer": tCustomerKey,
                                                                        "ipcountry": tIpStore.ipCountry } )
        
            
    def IpInfoScraper(self, pIp):
        tIpUrl = 'http://whatismyipaddress.com/ip/'
        tIpUrl = tIpUrl + pIp
        #logging.debug("Ip Url: " + tIpUrl)
        request_cookies = mechanize.CookieJar()
        request_opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(request_cookies))
        request_opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
        mechanize.install_opener(request_opener)
        tResponse = mechanize.urlopen(url = tIpUrl, timeout = 25.0)
        tContent = str(urllib.unquote(tResponse.read()))
        #logging.debug(str(tContent))
        tCity = ""
        tCountry = ""
        tProxy = ""
        tHost = ""
        tIsp = ""
        tState = ""
        tType = ""
        
        try:
            tCountryRegex = re.compile("<th>Country:</th><td>(?P<country>.*) <img")
            tCountryMatch = tCountryRegex.search(tContent)
            tCountry = tCountryMatch.groupdict()['country']
        except:
            logging.debug("Country Storing Failed")
        
        try:
            tHostRegex = re.compile("<th>Hostname:</th><td>(?P<host>.*)</td></tr><tr><th>I")
            tHostMatch = tHostRegex.search(tContent)
            tHost = tHostMatch.groupdict()['host']
        except:
            logging.debug("Host Storing Failed")
        
        try:
            tStateRegex = re.compile("<th>State/Region:</th><td>(?P<state>.*)</td></tr>")
            tStateMatch = tStateRegex.search(tContent)
            tState = tStateMatch.groupdict()['state']
        except:
            logging.debug("State Storing Failed")
        
        try:
            tCityRegex = re.compile("<th>City:</th><td>(?P<city>.*)</td></tr>")
            tCityMatch = tCityRegex.search(tContent)
            tCity = tCityMatch.groupdict()['city']
        except:
            logging.debug("City Storing Failed")
        
        try:
            tIspRegex = re.compile("<th>ISP:</th><td>(?P<isp>.*)</td></tr><tr><th>Or")
            tIspMatch = tIspRegex.search(tContent)
            tIsp = tIspMatch.groupdict()['isp']
        except:
            logging.debug("ISP Storing Failed")

        try:
            tProxyRegex = re.compile("<th>Services:</th><td>(?P<proxy>.*)</td></tr><tr><th>T")
            tProxyMatch = tProxyRegex.search(tContent)
            tProxy = tProxyMatch.groupdict()['proxy']
            if(tProxy[0] == "<"):
                tProxyRegex = re.compile('<a href="/ip-services">(?P<proxy>.*)</a>')
                tProxyMatch = tProxyRegex.search(tProxy)
                tProxy = tProxyMatch.groupdict()['proxy']
        except:
            logging.debug("Proxy Storing Failed")
        
        try:
            tTypeRegex = re.compile("<th>Type:</th><td><a.+href=[\'|\"](.+)[\'|\"].*?>(?P<type>.*)</a></td></tr><tr><th>A")
            tTypeMatch = tTypeRegex.search(tContent)
            tType = tTypeMatch.groupdict()['type']
        except:
            logging.debug("Type Storing Failed")
        
        tResult = {}
        tResult['country'] = tCountry
        tResult['host'] = tHost
        tResult['state'] = tState
        tResult['isp'] = tIsp
        tResult['proxy'] = tProxy
        tResult['type'] = tType
        
        return tResult
    
    def GetIp(self, pIpString):
        tIpQuery = None
        tIpQueryString = None
        tIpResults = []
        tIpQueryString = "Select * from IpInfo where ip = '" + str(pIpString) + "'"
        tIpQuery = db.GqlQuery(tIpQueryString)
        tIpResults = tIpQuery.fetch(1)
        return tIpResults
    
    def GetChargebacks(self, pIp):
        tOrderQueryString = "SELECT * FROM Order WHERE orderIp = '" + str(pIp) + "' and orderChargeback = 'True'"
        tOrderQuery = db.GqlQuery(tOrderQueryString)
        tOrderResults = tOrderQuery.fetch(100)
        return tOrderResults
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            