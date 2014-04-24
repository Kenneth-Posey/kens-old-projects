import logging
from base import BaseHandler
from _data import TierContainer
from models.vipsubscription import VipSubscription
from models.vipsubscriber import VipSubscriber

class VipList(BaseHandler):
    LOCATION = "../views/viplist.html"
    def GetContext(self):
        tContext = {}
        
        tDic = VipList.GetVips("Tier1")
        tSubList = []
        tSubscription = VipSubscription()
        tSubscriber = VipSubscriber()
        
        for tSubscription in tDic["Tier1"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            #logging.debug("Subscription: " + tSubscription.subscriptionOwner)
            #logging.debug("Subscriber: " + tSubscriber.subscriberEmail)
            tSubList.append(tTuple)
        
        tDic["Tier1"] = tSubList
        tContext.update(tDic)
        
        tDic = VipList.GetVips("Tier2")
        tSubList = []
        for tSubscription in tDic["Tier2"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            #logging.debug("Subscription: " + tSubscription.subscriptionOwner)
            #logging.debug("Subscriber: " + tSubscriber.subscriberEmail)
            tSubList.append(tTuple)
        
        tDic["Tier2"] = tSubList
        tContext.update(tDic)
        
        tDic = VipList.GetVips("Tier3")
        tSubList = []
        for tSubscription in tDic["Tier3"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            #logging.debug("Subscription: " + tSubscription.subscriptionOwner)
            #logging.debug("Subscriber: " + tSubscriber.subscriberEmail)
            tSubList.append(tTuple)
        
        tDic["Tier3"] = tSubList
        tContext.update(tDic)                


        tDic = VipList.GetVips("Tier4")
        tSubList = []
        for tSubscription in tDic["Tier4"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            #logging.debug("Subscription: " + tSubscription.subscriptionOwner)
            #logging.debug("Subscriber: " + tSubscriber.subscriberEmail)
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
        tVipSubQuery.filter("subscriptionManualState", tier)
        tVipSubQuery.order("subscriptionStart")
        tTierVips = tVipSubQuery.fetch(limit=500)
        #logging.debug("Tier " + tier + " vips")
        #logging.debug(str(tTierVips))
        tDic = { tier : tTierVips }
        return tDic