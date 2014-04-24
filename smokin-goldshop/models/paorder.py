from google.appengine.ext import db

class PaOrder(db.Expando):
    paDate = db.DateTimeProperty(auto_now_add=True)
    paDateDelivered = db.DateTimeProperty(auto_now=True)
    paAmount = db.StringProperty()
    paAmountInt = db.IntegerProperty()
    paTransactionId = db.StringProperty()
    paDeliveryAgent = db.StringProperty()
    paDeliveryAgentNick = db.StringProperty()
    paAssignedAgent = db.StringProperty()
    paAssignedAgentNick = db.StringProperty()
    paDeliveryDate = db.DateTimeProperty()
    paOrderDeliver = db.BooleanProperty(default=False)
    paOrderLock = db.BooleanProperty(default=False)