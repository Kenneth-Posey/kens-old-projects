import logging
from google.appengine.ext import webapp
from models.vipsubscription import VipSubscription
from _timemethods import TimeHelperMethods
from _data import TierContainer

class VipUpgradeMonitor(webapp.RequestHandler):
    def get(self):
        #logging.debug("===== VIP Upgrade Monitor Launched =====")
        
        tVip = VipSubscription()
        tSubscriptionTierGrades = {
                                "Tier1": ("Tier0", (0, 30)),
                                "Tier2": ("Tier1", (31, 60)),
                                "Tier3": ("Tier2", (61, 120)),
                                "Tier4": ("Tier3", (121, 5000))
                                }
        
        tSubscriptionTierGrades = TierContainer.GetVipTierInfo()
        tSortedKeys = sorted(tSubscriptionTierGrades.keys())
        
        #logging.debug("Tiers: " + str(tSortedKeys))
        
        for tier in tSortedKeys:
            #establish parameters for vips that need upgrading
            tMinDays = tSubscriptionTierGrades[tier][1][0]
            tMaxDays = tSubscriptionTierGrades[tier][1][1]
            tOldTier = tSubscriptionTierGrades[tier][0]

            #logging.debug("Old Tier: " + str(tOldTier))   
            #logging.debug("Min Days: " + str(tMinDays))
            #logging.debug("New Tier: " + str(tier))         
            #logging.debug("Max Days: " + str(tMaxDays))
            
            tMinDaysAgo = TimeHelperMethods.DaysAgo(tMinDays)
            tMaxDaysAgo = TimeHelperMethods.DaysAgo(tMaxDays)
            
            #logging.debug("Min Days Ago: " + str(tMinDaysAgo))
            #logging.debug("Max Days Ago: " + str(tMaxDaysAgo))
            
            tVipSubQuery = VipSubscription.all()
            tVipSubQuery.filter("subscriptionStart <=", tMinDaysAgo)
            tVipSubQuery.filter("subscriptionStart >=", tMaxDaysAgo)
            tVipSubQuery.filter("subscriptionIsActive", True)
            tVipSubQuery.filter("subscriptionAutoState", tOldTier)
            
            tVipList = tVipSubQuery.fetch(limit=100)
            
            #logging.debug("Vip List: " + str(tVipList))
            
            #these are vips that need to be auto-updated
            if(tVipList != None and len(tVipList) > 0):
                for tVip in tVipList:
                    if (tVip.subscriptionAutoState == tVip.subscriptionManualState and tVip.subscriptionManualState != 'Tier0'):
                        if (tVip.subscriptionNeedsUpgrade != False):
                            tVip.subscriptionNeedsUpgrade = False
                            tVip.put()
                    else:
                        tVip.subscriptionAutoState = tier
                        tVip.subscriptionNeedsUpgrade = True
                        tVip.put()
                    
                    
class VipUpgradeScript(webapp.RequestHandler):
    def get(self):
        #logging.debug("===== VIP Upgrade Script Launched =====")
        
        tVip = VipSubscription()
        tSubscriptionTierGrades = {
                                "Tier1": ("Tier0", (0, 30)),
                                "Tier2": ("Tier1", (31, 60)),
                                "Tier3": ("Tier2", (61, 120)),
                                "Tier4": ("Tier3", (121, 5000))
                                }
        
        tSubscriptionTierGrades = TierContainer.GetVipTierInfo()
        tSortedKeys = sorted(tSubscriptionTierGrades.keys())
        
        #logging.debug("Tiers: " + str(tSortedKeys))
        
        for tier in tSortedKeys:
            #logging.debug("Tier: " + str(tier))
            
            tVipSubQuery = VipSubscription.all()
            tVipSubQuery.filter("subscriptionAutoState", tier)
            tVipSubQuery.filter("subscriptionManualState", tier)
            tVipSubQuery.filter("subscriptionNeedsUpgrade", True)
            
            tVipList = tVipSubQuery.fetch(limit=100)
            
            #logging.debug("Vip List: " + str(tVipList))
            
            for tVipSub in tVipList:
                tVipSub.subscriptionNeedsUpgrade = False
                tVipSub.put()