import logging
import urllib
from models.vipsubscription import VipSubscription
from models.vipsubscriber import VipSubscriber
from baseajax import BaseAjax
from google.appengine.ext import webapp
from public import mechanize

class VipCancelPaypalAjax(BaseAjax):
    
    #Modified for account security
    API_PASSWORD  = "REDACTED"
    API_USERNAME  = "REDACTED"
    API_SIGNATURE = "REDACTED"
    
    def PostContext(self):
        tResponse = {}
        tResponse['tResponseText'] = ""
        tPaypal = VipCancelPaypalAjax()
        tResultDictionary = {}
        tPaypalPayload = {}        
        tPayload = {}
        
        pSubscriptionKey = str(self.request.get('key'))
        tSubscription = VipSubscription()
        try:
            tSubscription = VipSubscription.get(pSubscriptionKey)
        except:
            tResponse['tResponseText'] = "Not Found"
            return tResponse
        #logging.debug("Subscription found with owner: " + tSubscription.subscriptionOwner)
        
        if (tSubscription):            
                    
            tPaypalPayload['METHOD'] = "ManageRecurringPaymentsProfileStatus"
            tPaypalPayload['PROFILEID'] = str(tSubscription.subscriptionId) 
            tPaypalPayload['ACTION'] = 'Cancel'
            
            tPayloadEncoded = tPaypal.GeneratePayload(tPaypalPayload)                
            
            request_cookies = mechanize.CookieJar()
            request_opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(request_cookies))
            request_opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
            mechanize.install_opener(request_opener)
                
            tResponse = mechanize.urlopen(url = tUrl, timeout = 25.0, data = tPayloadEncoded)
            tResult = str(urllib.unquote(tResponse.read()))
            
            #logging.debug("Mechanize Package")
            #logging.debug("Url: " + tUrl)
            #logging.debug("Data: " + str(tPaypalPayload))
            #logging.debug("Response: " + tResult)
            
            tResultSplit = tResult.split('&')
            
            for tPair in tResultSplit:
                tSplitPair = tPair.split("=")
                tResultDictionary[tSplitPair[0]] = tSplitPair[1]
            
            tResponse['tResponseText'] = "Cancelled"
            
            tSubscription.subscriptionIsActive = False
            tSubscription.subscriptionEnd = datetime.datetime.now()        
            tSubscription.subscriptionNeedsUpgrade = False
            tSubscription.subscriptionNeedsCancel = False
            tSubscription.put()    
            
            tSubscriber = VipSubscriber()
            tSubscriber.subscriberActiveSubscription = ""
            tSubscriber.subscriberHasActiveSubscription = False
            tSubscriber.put()
            
        return tResponse
    
    def GeneratePayload(self, pPayload):
        tPayload = {}
        tPayload = pPayload
        tBasePayload = {
            "USER" : self.API_USERNAME,
            "PWD" : self.API_PASSWORD,
            "SIGNATURE" : self.API_SIGNATURE,
            "VERSION" : "72.0"
            }
        
        for tKey in tPayload.keys():
            tBasePayload[tKey] = tPayload[tKey]
        
        return urllib.urlencode(tBasePayload)