from google.appengine.ext import db

class StockTransaction(db.Expando):
    transOwner = db.StringProperty(default='')    
    transComment = db.StringProperty(default='')
    
    transGoldType = db.StringProperty(default='')
    transGoldAmount = db.IntegerProperty(default=0)
    
    transDate = db.DateTimeProperty(auto_now_add=True)
    
    transSkippedCommission = db.BooleanProperty(default=False)
    
    transTarget = db.StringProperty(default='')