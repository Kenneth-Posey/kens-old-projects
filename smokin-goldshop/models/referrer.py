from google.appengine.ext import db

class Referrer(db.Expando):
    referGp = db.FloatProperty()
    referCash = db.FloatProperty()
    referEmail = db.StringProperty()
    referPin = db.StringProperty()
    referId = db.StringProperty()
    referSimpleGold = db.StringProperty()
    referSimpleCash = db.StringProperty()