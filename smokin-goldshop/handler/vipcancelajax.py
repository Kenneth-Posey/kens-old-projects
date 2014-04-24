import logging
from models.vipsubscription import VipSubscription
from baseajax import BaseAjax

class VipCancel(BaseAjax):
    def post(self):
        tResponse = {}
        tResponse['tResponseText'] = ""
        
        pSubscriptionKey = str(self.request.get('key'))
        tSubscription = VipSubscription()
        try:
            tSubscription = VipSubscription.get(pSubscriptionKey)
        except:
            tResponse['tResponseText'] = "Not Found"
            return tResponse
        #logging.debug("Subscription found with owner: " + tSubscription.subscriptionOwner)
        tier = ""
        if (tSubscription):
            tSubscription.subscriptionNeedsUpgrade = False
            tSubscription.subscriptionNeedsCancel = False
            tSubscription.put()
        #logging.debug("Subscription Cancelled")
        
        tResponse['tResponseText'] = "Cancelled"
        
        return tResponse        