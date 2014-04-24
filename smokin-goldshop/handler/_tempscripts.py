from models.vipsubscription import VipSubscription
from base import BaseHandler

class ResetVip(BaseHandler):
    LOCATION = "../views/index.html"
    def GetContext(self):
        tVip = VipSubscription()
        
        tVipQuery = VipSubscription.all()
        tVipQuery.filter("subscriptionAutoState", "Tier0")
        
        tVips = tVipQuery.fetch(limit = 300)
        
        for tVip in tVips:
            tVip.subscriptionAutoState = "Tier0"
            tVip.put()
        
        return {}