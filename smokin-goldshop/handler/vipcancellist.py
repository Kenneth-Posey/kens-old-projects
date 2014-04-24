import logging
from base import BaseHandler
from _data import TierContainer
from models.vipsubscription import VipSubscription
from models.vipsubscriber import VipSubscriber

class VipCancelList(BaseHandler):
    LOCATION = "../views/vipcancellist.html"
    def GetContext(self):
        tContext = {}
        
        tDic = VipCancelList.GetVips("Tier1")
        tSubList = []
        for tSubscription in tDic["Tier1"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            tSubList.append(tTuple)
        
        tDic["Tier1"] = tSubList
        tContext.update(tDic)
        
        tDic = VipCancelList.GetVips("Tier2")
        tSubList = []
        for tSubscription in tDic["Tier2"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            tSubList.append(tTuple)
        
        tDic["Tier2"] = tSubList
        tContext.update(tDic)
        
        tDic = VipCancelList.GetVips("Tier3")
        tSubList = []
        for tSubscription in tDic["Tier3"]:
            tSubscriber = VipSubscriber.GetSubscriberById(tSubscription.subscriptionOwner)
            tTuple = (tSubscriber, tSubscription)
            tSubList.append(tTuple)
        
        tDic["Tier3"] = tSubList
        tContext.update(tDic)                


        tDic = VipCancelList.GetVips("Tier4")
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
        tVipSubQuery.filter("subscriptionNeedsCancel", True)
        tVipSubQuery.filter("subscriptionAutoState", tier)
        tVipSubQuery.order("subscriptionEnd")
        tTierVips = tVipSubQuery.fetch(limit=100)
        tDic = { tier : tTierVips }
        return tDic
    