from google.appengine.ext import db

class DonorRecord(db.Expando):
    donorGoldAmount = db.IntegerProperty()
    donorRsName = db.StringProperty(default = "")
    donorForumName = db.StringProperty(default = "")
    donorMemo = db.StringProperty(multiline=True)
    donorDate = db.DateTimeProperty(auto_now_add = True)
    donorAgent = db.StringProperty()