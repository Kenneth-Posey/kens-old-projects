import logging
from google.appengine.ext import db

class Promo(db.Expando):
    promoGoldAmount = db.IntegerProperty()
    promoPercentage = db.FloatProperty()
    promoUses = db.IntegerProperty()
    promoLimit = db.IntegerProperty()
    promoName = db.StringProperty()
    promoOrders = db.StringListProperty()
    promoCode = db.StringProperty()
    promoIsActive = db.BooleanProperty()
    
    @staticmethod
    def GetPromoByCode(pCode):
        tPromoQuery = Promo().all()
        tPromoQuery.filter("promoIsActive", True)
        tPromoQuery.filter("promoCode", pCode.lower())
        #logging.debug("PromoCode: " + str(pCode))
        tPromo = tPromoQuery.fetch(1)
        
        if(len(tPromo) != 0):
            return tPromo[0]    
        