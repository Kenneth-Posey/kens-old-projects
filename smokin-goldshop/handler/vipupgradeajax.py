import logging
from models.vipsubscription import VipSubscription
from baseajax import BaseAjax

class VipUpgradeAjax(BaseAjax):
    def PostContext(self):
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
            #logging.debug("Manual State: " + tSubscription.subscriptionManualState)
            #logging.debug("Needs Upgrade: " + str(tSubscription.subscriptionNeedsUpgrade))
            if (tSubscription.subscriptionManualState == "Tier0"):
                tSubscription.subscriptionManualState = "Tier1"
                tSubscription.subscriptionNeedsUpgrade = False
                tier="Tier 1"
                tSubscription.put()
            elif(tSubscription.subscriptionManualState == "Tier1"):
                tSubscription.subscriptionManualState = "Tier2"
                tSubscription.subscriptionNeedsUpgrade = False
                tier="Tier 2"
                tSubscription.put()
            elif(tSubscription.subscriptionManualState == "Tier2"):
                tSubscription.subscriptionManualState = "Tier3"
                tSubscription.subscriptionNeedsUpgrade = False
                tier="Tier 3"
                tSubscription.put()
            elif(tSubscription.subscriptionManualState == "Tier3"):
                tSubscription.subscriptionManualState = "Tier4"
                tSubscription.subscriptionNeedsUpgrade = False
                tier = "Tier 4"
                tSubscription.put()
            elif(tSubscription.subscriptionManualState == "Tier4"):
                tSubscription.subscriptionManualState = "Tier4"
                tSubscription.subscriptionNeedsUpgrade = False
                tier="Tier 4"
                tSubscription.put()
            elif(tSubscription.subscriptionManualState == tSubscription.subscriptionAutoState):
                if(tSubscription.subscriptionNeedsUpgrade == True):
                    tSubscription.subscriptionNeedsUpgrade = False
                    tSubscription.put()
            #logging.debug("Manual State: " + tSubscription.subscriptionManualState)
            #logging.debug("Needs Upgrade: " + str(tSubscription.subscriptionNeedsUpgrade))
        #logging.debug("Subscription Saved at Tier " + tier)
        
        tResponse['tResponseText'] = "=> " + tier
        
        return tResponse