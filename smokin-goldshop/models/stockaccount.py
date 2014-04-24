from google.appengine.ext import db

class StockAccount(db.Expando):
    
    stockQuantityEoc = db.IntegerProperty(default=0)
    stockQuantity07 = db.IntegerProperty(default=0)
        
    stockName = db.StringProperty(default='primary')
    
    stockLastChanged = db.DateTimeProperty(auto_now=True)
    stockCreated = db.DateTimeProperty(auto_now_add=True)
    
    stockCommission = db.FloatProperty(default=0.0)
    
    stockPrice07 = db.FloatProperty(default=0.0)
    stockPriceEoc = db.FloatProperty(default=0.0)