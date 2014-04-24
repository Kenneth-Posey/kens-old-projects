from google.appengine.ext import db

class CustomerMaster(db.Expando):
    masterMemo = db.StringProperty(multiline = True)
    masterIsPaBlacklisted = db.BooleanProperty()
    masterIsGlobalBlacklisted = db.BooleanProperty()
    
    #List of customer entity id
    masterCustomerList = db.StringListProperty(default=[])
    
    masterIpList = db.StringListProperty(default=[])
    masterPhoneList = db.StringListProperty(default=[])
    masterEmailList = db.StringListProperty(default=[])
    masterPaypalIdList = db.StringListProperty(default=[])
    masterRsnList = db.StringListProperty(default=[])
    