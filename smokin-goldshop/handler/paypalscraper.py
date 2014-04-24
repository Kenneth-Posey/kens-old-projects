
import os, datetime, urllib, urllib2, re, logging
from public import mechanize    
from google.appengine.api import memcache, users, taskqueue
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app
import json
from paypal import PaypalHandler

class PaypalScraper(webapp.RequestHandler):
    def get(self):
        tUrl = "https://api-3t.paypal.com/nvp"
        tOperation = "TransactionSearch"
        tOrderList = []
        tPaypalPayload = {}        
        tPayload = {}
        tPaypal = PaypalTrigger()
        tPostDate = self.request.get('date')
        
        if (tPostDate == None or tPostDate == ""):
            tPostDate = str(datetime.datetime(2011, 2, 1, 1, 01, 01))
            
        tStartDate = tPaypal.StringToDatetime(tPostDate)
        tIncrement = datetime.timedelta(days = 1)
        tEndDate = tStartDate + tIncrement
        if(int(tEndDate.day) > 31):
            tEndDate = datetime.datetime(tStartDate.year, str(int(tStartDate.month) + 1), "01",
                                         tStartDate.hour, tStartDate.minute, tStartDate.second)
        #logging.debug("Fetching Items for Date: " + str(tPaypal.DatetimeToString(tStartDate)))
        
        tPaypalPayload['TRANSACTIONCLASS'] = "Received"
        tPaypalPayload['STATUS'] = "Success"
        tPaypalPayload['METHOD'] = tOperation
        tPaypalPayload['STARTDATE'] = tStartDate
        tPaypalPayload['ENDDATE'] = tEndDate
        tPayloadEncoded = tPaypal.GeneratePayload(tPaypalPayload)
        
        request_cookies = mechanize.CookieJar()
        request_opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(request_cookies))
        request_opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
        mechanize.install_opener(request_opener)
        
        tResponse = mechanize.urlopen(url = tUrl, timeout = 25.0, data = tPayloadEncoded)
        #logging.debug("Mechanize Package")
        #logging.debug("Url: " + tUrl)
        #logging.debug("Data: " + str(tPaypalPayload))
        
        tResult = tResponse.read()
        #logging.debug(tResult)
        #except:
            #logging.error("Paypal Timed Out: " + str(tPaypal.DatetimeToString(tStartDate)))
            #tEndDate = tStartDate
            #tResult = ""
            
        tPayload['date'] = tPaypal.DatetimeToString(tEndDate)
        
        tTimestampRegex = re.compile("L_TIMESTAMP(?P<objectnumber>\d*)=(?P<timestamp>.*?)Z&")
        tTimestampMatches = tTimestampRegex.findall(tResult)
        
        for tTimestamp in tTimestampMatches:
            tTempOrder = Order()
            tTimestampDecoded = urllib.unquote(tTimestamp[1])
            tTimestampSplit = str(tTimestampDecoded).split('T')
            tTimestampDate = tTimestampSplit[0]
            tTimestampTime = tTimestampSplit[1]
            tTimestampDateSplit = tTimestampDate.split('-')
            tTimestampTimeSplit = tTimestampTime.split(':')
            
            tOrderTime = datetime.datetime(int(tTimestampDateSplit[0]), int(tTimestampDateSplit[1]), 
                                           int(tTimestampDateSplit[2]), int(tTimestampTimeSplit[0]),
                                           int(tTimestampTimeSplit[1]), int(tTimestampTimeSplit[2]))
            
            tTempOrder.orderCreated = tOrderTime
            tOrderList.append(tTempOrder)
        
        tTypeRegex = re.compile("L_TYPE(?P<objectnumber>\d*)=(?P<type>.*?)&")
        tTypeMatches = tTypeRegex.findall(tResult)
        
        for tType in tTypeMatches:
            tTempOrder = tOrderList[int(tType[0])]
            tTempOrder.orderPaypalType = urllib.unquote(tType[1])
            tOrderList[int(tType[0])] = tTempOrder
        
        tEmailRegex = re.compile("L_EMAIL(?P<objectnumber>\d*)=(?P<email>.*?)&")
        tEmailMatches = tEmailRegex.findall(tResult)
        
        for tEmail in tEmailMatches:
            tTempOrder = tOrderList[int(tEmail[0])]
            tTempOrder.orderCustomerEmail = urllib.unquote(tEmail[1])
            tOrderList[int(tEmail[0])] = tTempOrder
            
        tNameRegex = re.compile("L_NAME(?P<objectnumber>\d*)=(?P<name>.*?)&")
        tNameMatches = tNameRegex.findall(tResult)
            
        for tName in tNameMatches:
            tTempOrder = tOrderList[int(tName[0])]
            tTempOrder.orderCustomerName = urllib.unquote(tName[1])
            tOrderList[int(tName[0])] = tTempOrder
            
        tTransactionIdRegex = re.compile("L_TRANSACTIONID(?P<objectnumber>\d*)=(?P<transactionid>.*?)&")
        tTransactionIdMatches = tTransactionIdRegex.findall(tResult)
        
        for tTransactionId in tTransactionIdMatches:
            tTempOrder = tOrderList[int(tTransactionId[0])]
            tTempOrder.orderPaypalId = urllib.unquote(tTransactionId[1])
            tOrderList[int(tTransactionId[0])] = tTempOrder
            
        tStatusRegex = re.compile("L_STATUS(?P<objectnumber>\d*)=(?P<status>.*?)&")
        tStatusMatches = tStatusRegex.findall(tResult)
        
        for tStatus in tStatusMatches:
            tTempOrder = tOrderList[int(tStatus[0])]
            tTempOrder.orderPaypalStatus = urllib.unquote(tStatus[1])
            tOrderList[int(tStatus[0])] = tTempOrder
            
        for tOrder in tOrderList:
            try:
                tOrder.put()
            except:
                logging.error("============= Order Storing FAILED =============")
                logging.error("orderPaypalStatus: " + str(tOrder.orderPaypalStatus))
                logging.error("orderPaypalId: " + str(tOrder.orderPaypalId))
                logging.error("orderCustomerName: " + str(tOrder.orderCustomerName))
                logging.error("orderCustomerEmail: " + str(tOrder.orderCustomerEmail))
                logging.error("orderCreated: " + str(tPaypal.DatetimeToString(tOrder.orderCreated)))
            
        tFormerCount = int(self.request.get('former'))
        tOrderCount = len(tOrderList)
        #logging.debug("Former Count: " + str(tFormerCount) + "    Order Count: " + str(tOrderCount))
        if (tOrderCount == 0):
            tFormerCount += 1
        else:
            tFormerCount = 0
            
        tPayload['former'] = tFormerCount
            
        if (tFormerCount < 100):
            taskqueue.add(url = '/paypaltrigger', countdown = 10, params = tPayload)
        
    def post(self):
        tUrl = "https://api-3t.paypal.com/nvp"
        tOperation = "TransactionSearch"
        tOrderList = []
        tPaypalPayload = {}        
        tPayload = {}
        tPaypal = PaypalTrigger()
        tPostDate = self.request.get('date')
        
        if (tPostDate == None):
            tPostDate = datetime.datetime(2011, 2, 1, 1, 01, 01)
            
        tStartDate = tPaypal.StringToDatetime(tPostDate)
        try:
            tIncrement = datetime.timedelta(days = 1)
            tEndDate = tStartDate + tIncrement
            if(int(tEndDate.day) > 31):
                tEndDate = datetime.datetime(tStartDate.year, str(int(tStartDate.month) + 1), "01",
                                             tStartDate.hour, tStartDate.minute, tStartDate.second)
            #logging.debug("Fetching Items for Date: " + str(tPaypal.DatetimeToString(tStartDate)))
            
            tPaypalPayload['TRANSACTIONCLASS'] = "Received"
            tPaypalPayload['STATUS'] = "Success"
            tPaypalPayload['METHOD'] = tOperation
            tPaypalPayload['STARTDATE'] = tStartDate
            tPaypalPayload['ENDDATE'] = tEndDate
            tPayloadEncoded = tPaypal.GeneratePayload(tPaypalPayload)
            
            request_cookies = mechanize.CookieJar()
            request_opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(request_cookies))
            request_opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
            mechanize.install_opener(request_opener)
            
            tResponse = mechanize.urlopen(url = tUrl, timeout = 25.0, data = tPayloadEncoded)
            #logging.debug("Mechanize Package")
            #logging.debug("Url: " + tUrl)
            #logging.debug("Data: " + str(tPaypalPayload))
            
            tResult = tResponse.read()
            #logging.debug(tResult)
        except:
            logging.error("Paypal Timed Out: " + str(tPaypal.DatetimeToString(tStartDate)))
            tEndDate = tStartDate
            tResult = ""
            
        tPayload['date'] = tPaypal.DatetimeToString(tEndDate)
        
        tTimestampRegex = re.compile("L_TIMESTAMP(?P<objectnumber>\d*)=(?P<timestamp>.*?)Z&")
        tTimestampMatches = tTimestampRegex.findall(tResult)
        
        for tTimestamp in tTimestampMatches:
            tTempOrder = Order()
            tTimestampDecoded = urllib.unquote(tTimestamp[1])
            tTimestampSplit = str(tTimestampDecoded).split('T')
            tTimestampDate = tTimestampSplit[0]
            tTimestampTime = tTimestampSplit[1]
            tTimestampDateSplit = tTimestampDate.split('-')
            tTimestampTimeSplit = tTimestampTime.split(':')
            
            tOrderTime = datetime.datetime(int(tTimestampDateSplit[0]), int(tTimestampDateSplit[1]), 
                                           int(tTimestampDateSplit[2]), int(tTimestampTimeSplit[0]),
                                           int(tTimestampTimeSplit[1]), int(tTimestampTimeSplit[2]))
            
            tTempOrder.orderCreated = tOrderTime
            tOrderList.append(tTempOrder)
        
        tTypeRegex = re.compile("L_TYPE(?P<objectnumber>\d*)=(?P<type>.*?)&")
        tTypeMatches = tTypeRegex.findall(tResult)
        
        for tType in tTypeMatches:
            tTempOrder = tOrderList[int(tType[0])]
            tTempOrder.orderPaypalType = urllib.unquote(tType[1])
            tOrderList[int(tType[0])] = tTempOrder
        
        tEmailRegex = re.compile("L_EMAIL(?P<objectnumber>\d*)=(?P<email>.*?)&")
        tEmailMatches = tEmailRegex.findall(tResult)
        
        for tEmail in tEmailMatches:
            tTempOrder = tOrderList[int(tEmail[0])]
            tTempOrder.orderCustomerEmail = urllib.unquote(tEmail[1])
            tOrderList[int(tEmail[0])] = tTempOrder
            
        tNameRegex = re.compile("L_NAME(?P<objectnumber>\d*)=(?P<name>.*?)&")
        tNameMatches = tNameRegex.findall(tResult)
            
        for tName in tNameMatches:
            tTempOrder = tOrderList[int(tName[0])]
            tTempOrder.orderCustomerName = urllib.unquote(tName[1])
            tOrderList[int(tName[0])] = tTempOrder
            
        tTransactionIdRegex = re.compile("L_TRANSACTIONID(?P<objectnumber>\d*)=(?P<transactionid>.*?)&")
        tTransactionIdMatches = tTransactionIdRegex.findall(tResult)
        
        for tTransactionId in tTransactionIdMatches:
            tTempOrder = tOrderList[int(tTransactionId[0])]
            tTempOrder.orderPaypalId = urllib.unquote(tTransactionId[1])
            tOrderList[int(tTransactionId[0])] = tTempOrder
            
        tStatusRegex = re.compile("L_STATUS(?P<objectnumber>\d*)=(?P<status>.*?)&")
        tStatusMatches = tStatusRegex.findall(tResult)
        
        for tStatus in tStatusMatches:
            tTempOrder = tOrderList[int(tStatus[0])]
            tTempOrder.orderPaypalStatus = urllib.unquote(tStatus[1])
            tOrderList[int(tStatus[0])] = tTempOrder
            
        for tOrder in tOrderList:
            try:
                tOrder.put()
            except:
                logging.error("============= Order Storing FAILED =============")
                logging.error("orderPaypalStatus: " + str(tOrder.orderPaypalStatus))
                logging.error("orderPaypalId: " + str(tOrder.orderPaypalId))
                logging.error("orderCustomerName: " + str(tOrder.orderCustomerName))
                logging.error("orderCustomerEmail: " + str(tOrder.orderCustomerEmail))
                logging.error("orderCreated: " + str(tPaypal.DatetimeToString(tOrder.orderCreated)))
            
        tFormerCount = int(self.request.get('former'))
        tOrderCount = len(tOrderList)
        #logging.debug("Former Count: " + str(tFormerCount) + "    Order Count: " + str(tOrderCount))
        if (tOrderCount == 0):
            tFormerCount += 1
        else:
            tFormerCount = 0
            
        tPayload['former'] = tFormerCount
            
        if (tFormerCount < 100):
            taskqueue.add(url = '/paypaltrigger', countdown = 10, params = tPayload)
        
        
        