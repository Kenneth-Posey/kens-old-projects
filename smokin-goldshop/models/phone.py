from google.appengine.ext import db

class Phone(db.Expando):
    phoneOrder = db.StringProperty()
    phoneCountry = db.StringProperty()
    phoneNumber = db.StringProperty()
    phoneState = db.StringProperty()
    phoneCustomer = db.StringProperty()
