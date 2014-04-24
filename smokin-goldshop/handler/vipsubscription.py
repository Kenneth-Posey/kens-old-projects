import urllib
from models.vipsubscription import VipSubscription as VipSub
from base import BaseHandler

class VipSubscription(BaseHandler):
    LOCATION = "../views/vipsubscription.html"
    def GetContext(self):
        tContext = {}
        tVipList = []
        
        tVipKey = urllib.unquote(self.request.get('key'))
        if(tVipKey != None and len(tVipKey) > 0):
            tVip = VipSub.get(tVipKey)
            tContext['tSub'] = tVip
        return tContext