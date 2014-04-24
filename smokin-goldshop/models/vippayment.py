from google.appengine.ext import db

class VipPayment(db.Expando):
    paymentPaypalId = db.StringProperty(default="")
    paymentEmail = db.StringProperty(default="")
    paymentForumName = db.StringProperty(default="")
    paymentAmount = db.StringProperty()
    paymentDate = db.DateTimeProperty(auto_now_add=True)