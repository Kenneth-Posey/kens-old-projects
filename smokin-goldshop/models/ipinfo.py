from google.appengine.ext import db
    
class IpInfo(db.Expando):
    ip = db.StringProperty()
    ipState = db.StringProperty()
    ipCountry = db.StringProperty()
    ipIsp = db.StringProperty()
    ipType = db.StringProperty()
    ipHost = db.StringProperty()
    ipProxy = db.StringProperty()
    ipOrder = db.StringProperty()
    ipDateChecked = db.DateTimeProperty(auto_now_add = True)
    ipIsGlobalBlacklisted = db.BooleanProperty()
    ipIsPaBlacklisted = db.BooleanProperty()