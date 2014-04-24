from google.appengine.ext import db
from agent import Agent
import logging

class ManualStockChange(db.Expando):
    stockCreated = db.DateTimeProperty(auto_now_add = True)
    stockIsGenerated = db.BooleanProperty(default=False)
    
    stockCreator = db.StringProperty(default='')
    stockRecipient = db.StringProperty(default='')
    
    #stockPromoCode = db.StringProperty(default='')
    #stockPromoGoldAmount = db.IntegerProperty(default=0)
    
    stockGoldType = db.StringProperty(default='') #eoc or 07
    stockGoldAmount = db.IntegerProperty(default=0)
    stockGoldAmountPretty = db.StringProperty(default='')
    
    #orderCashValue = db.FloatProperty(default=0.0)
    stockComments = db.StringProperty(default='', multiline=True)