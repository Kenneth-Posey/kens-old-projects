import logging
import urllib
from models.vipsubscription import VipSubscription
from models.vipsubscriber import VipSubscriber
from baseajax import BaseAjax
from google.appengine.ext import webapp
from public import mechanize

class VipRefundPaypalAjax(BaseAjax):
    
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
        
        