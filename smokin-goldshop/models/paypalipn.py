from google.appengine.ext import db

class PaypalIPN(db.Expando):
    ipnMessageSent = db.DateTimeProperty(auto_now_add=True)
    ipnRawMessage = db.TextProperty()