from google.appengine.ext import db

class VipSubscriber(db.Expando):
    subscriberPaypalId = db.StringProperty(default="")
    subscriberEmail = db.StringProperty(default="")
    subscriberForumName = db.StringProperty(default="")
    subscriberSubscriptions = db.StringListProperty()
    subscriberHasActiveSubscription = db.BooleanProperty(default = False)
    subscriberActiveSubscription = db.StringProperty(default="")
    subscriberCreated = db.DateTimeProperty(auto_now_add=True)
    
    @staticmethod
    def GetActiveSubscribers():
        tSubscriber = VipSubscriber()
        tSubscriberBl = VipSubscriber.all()
        tSubscriberBl.filter("subscriberHasActiveSubscription", True)
        tSubscriberBl.order("-subscriberCreated")
        return tSubscriberBl.fetch(limit=100)
    
    @staticmethod
    def GetSubscriberById(pPaypalId):
        tSubscriber = VipSubscriber()
        tSubscriberBl = VipSubscriber.all()
        tSubscriberBl.filter("subscriberPaypalId", pPaypalId)
        tSubscriberList = tSubscriberBl.fetch(limit=1)
        
        if (len(tSubscriberList) > 0):
            return tSubscriberList[0]
        else:
            tSubscriber.subscriberPaypalId = pPaypalId
            #tSubscriber.put()
            return tSubscriber        
        
    @staticmethod
    def GetSubscriberByIdAndEmail(pPaypalId, pPaypalEmail):
        tSubscriber = VipSubscriber()
        tSubscriberBl = VipSubscriber.all()
        tSubscriberBl.filter("subscriberPaypalId", pPaypalId)
        tSubscriberBl.filter("subscriberEmail", pPaypalEmail)
        tSubscriberList = tSubscriberBl.fetch(limit=1)
        
        if (len(tSubscriberList) > 0):
            return tSubscriberList[0]
        else:
            tSubscriber.subscriberPaypalId = pPaypalId
            tSubscriber.subscriberEmail = pPaypalEmail
            tSubscriber.put()
            return tSubscriber
    
    @staticmethod
    def GetSubscriberActiveSubscriptions(pSubscriber):
        tSubscriber = VipSubscriber()
        tSubscriber = pSubscriber
        tSubscriptionList = []
        tSubscriptions = VipSubscriber.all()
        tSubscriptions.filter("subscriptionOwner", tSubscriber.subscriberPaypalId)
        tSubscriptions.filter("subscriptionAutoState", True)
        tSubscriptionList = tSubscriptions.fetch()
        
        return tSubscriptionList
        
    
    
    
    