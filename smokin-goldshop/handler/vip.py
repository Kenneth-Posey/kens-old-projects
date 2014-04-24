import urllib
from models.vipsubscriber import VipSubscriber
from base import BaseHandler

class Vip(BaseHandler):
    LOCATION = "../views/vip.html"
    def GetContext(self):
        tContext = {}
        tVipList = []
        
        tVipKey = urllib.unquote(self.request.get('key'))
        if(tVipKey != None and len(tVipKey) > 0):
            tVip = VipSubscriber.get(tVipKey)
            tContext['tVip'] = tVip
        return tContext
    
    def PostContext(self):
        tContext = {}
        tVip = VipSubscriber()
        
        tVipForumName = urllib.unquote(self.request.get('forumname'))
        tVipKey = urllib.unquote(self.request.get('key'))
        if(tVipKey != None and len(tVipKey) > 0):
            tVip = VipSubscriber.get(tVipKey)
            tContext['tVip'] = tVip
        
        if(tVipForumName != None and len(tVipForumName) > 0):
            tVip.subscriberForumName = tVipForumName
            
        tVip.put()
        
        return tContext