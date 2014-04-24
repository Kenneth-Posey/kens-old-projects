from google.appengine.ext import db

class VipSubscription(db.Expando):
    subscriptionId = db.StringProperty()
    subscriptionOwner = db.StringProperty() #paypal buyer id
    subscriptionOwnerKey = db.StringProperty() #database owner key
    subscriptionStart = db.DateTimeProperty(auto_now_add=True)
    subscriptionEnd = db.DateTimeProperty()
    subscriptionLastPaid = db.DateTimeProperty(auto_now=True)
    subscriptionAutoState = db.StringProperty(default="Tier0")
    subscriptionManualState = db.StringProperty(default="Tier0") 
    subscriptionNeedsUpgrade = db.BooleanProperty(default=False)
    subscriptionIsActive = db.BooleanProperty(default=False)
    subscriptionLog = db.StringListProperty()
    subscriptionNeedsCancel = db.BooleanProperty(default=False)
    
    @staticmethod
    def GetActiveSubscriptionsByOwner(pPaypalId):
        tVipSubQuery = VipSubscription.all()
        tVipSubQuery.filter("subscriptionIsActive", True)
        tVipSubQuery.filter("subscriptionOwner", pPaypalId)
        
        tVipSub = tVipSubQuery.fetch(limit = 1)
        return tVipSub
        
    @staticmethod
    def GetActiveSubscriptions():
        tVipSubQuery = VipSubscription.all()
        tVipSubQuery.filter("subscriptionIsActive", True)
        
        tVipSub = tVipSubQuery.fetch(limit = 200)
        return tVipSub
    
    