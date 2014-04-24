import logging
from base import BaseHandler
from _data import TierContainer
from models.vipsubscription import VipSubscription
from models.vipsubscriber import VipSubscriber

class VipUpgradeList(BaseHandler):
    LOCATION = "../views/upgradelist.html"
    def GetContext(self):
        tContext = {}
        
        tDic = VipUpgradeList.GetVips("Tier1")
        tSubList = []
        for tSubscription in tDic["Tier1"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            tSubList.append(tTuple)
        
        tDic["Tier1"] = tSubList
        tContext.update(tDic)
        
        tDic = VipUpgradeList.GetVips("Tier2")
        tSubList = []
        for tSubscription in tDic["Tier2"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            tSubList.append(tTuple)
        
        tDic["Tier2"] = tSubList
        tContext.update(tDic)
        
        tDic = VipUpgradeList.GetVips("Tier3")
        tSubList = []
        for tSubscription in tDic["Tier3"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            tSubList.append(tTuple)
        
        tDic["Tier3"] = tSubList
        tContext.update(tDic)                


        tDic = VipUpgradeList.GetVips("Tier4")
        tSubList = []
        for tSubscription in tDic["Tier4"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            tSubList.append(tTuple)
        
        tDic["Tier4"] = tSubList
        tContext.update(tDic)                
        #logging.debug(str(tContext))
            
        return tContext
    
    @staticmethod
    def GetVips(tier):
        tVip = VipSubscription()
        tVipSubQuery = VipSubscription.all()
        tVipSubQuery.filter("subscriptionIsActive", True)
        tVipSubQuery.filter("subscriptionAutoState", tier)
        tVipSubQuery.filter("subscriptionNeedsUpgrade", True)
        tVipSubQuery.order("subscriptionStart")
        tTierVips = tVipSubQuery.fetch(limit=100)
        tDic = { tier : tTierVips }
        return tDic
    