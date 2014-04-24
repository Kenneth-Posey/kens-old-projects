from google.appengine.ext import db

class CustomerNew(db.Expando):
    customerFirstName = db.StringProperty(default="")
    customerLastName = db.StringProperty(default="")
    
    customerAddress = db.StringProperty(default="")
    customerCity = db.StringProperty(default="")
    customerState = db.StringProperty(default="")
    customerCountry = db.StringProperty(default="")
    
    customerEmail = db.StringProperty(default="")
    customerPhone = db.StringProperty(default="")    
    
    customerAccounts = db.StringListProperty(default=[])
    customerIpAddresses = db.StringListProperty(default=[])
    customerOrders = db.StringListProperty(default=[])
    customerOrderCount = db.IntegerProperty(default=0)
    customerChargebacks = db.StringListProperty(default=[])
    customerChargebackCount = db.IntegerProperty(default=0)
    
    customerPhoneVerified = db.BooleanProperty(default=False)
    customerPhoneVerificationNumber = db.StringProperty(default="")
    customerEmailVerified = db.BooleanProperty(default=False)
    customerEmailVerificationNumber = db.StringProperty(default="")
    customerIdVerified = db.BooleanProperty(default=False)
    customerIdPhoto = db.Blob()
    customerIdLink = db.StringProperty(default="")
    customerPaypalId = db.StringProperty(default="")
    customerMemo = db.StringProperty(multiline=True)
    customerIsPaBlacklisted = db.BooleanProperty(default=False)
    customerIsGlobalBlacklisted = db.BooleanProperty(default=False)
    customerUsedBonus = db.StringListProperty(default=[])
    
    customerOriginalKey = db.StringProperty(default="")
    customerMaster = db.StringProperty(default="")