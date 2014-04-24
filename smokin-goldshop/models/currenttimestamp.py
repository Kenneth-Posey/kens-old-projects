from google.appengine.ext import db
    
class CurrentTimestamp(db.Expando):
    currentTimestamp = db.DateTimeProperty()
    currentTimestampLocked = db.BooleanProperty()