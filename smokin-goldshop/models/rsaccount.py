from google.appengine.ext import db

class RsAccount(db.Expando):
    accountName = db.StringProperty()
    accountOwners = db.StringListProperty()
    accountBalance = db.IntegerProperty()
    accountPin = db.StringProperty()