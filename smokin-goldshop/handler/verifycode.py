import re, logging, json, webapp2
from models.price import Price
from models.order import Order
from _data import PriceContainer

class VerifyCode(webapp2.RequestHandler):
    def get(self):
        tCode = re.sub(r'\W', '', self.request.get('code')).lower()
        tOrderId = self.request.get('id')
        
        logging.debug(tCode)
        
        tOrder = Order()
        #tOrder.orderVerificationCode
        tOrderQuery = Order().all()
        tOrderQuery.filter('orderVerificationCode', tCode)
        
        if(tOrderId):
            tOrderQuery.filter('orderTransactionId', tOrderId)
        
        tOrderList = tOrderQuery.fetch(limit=1)
        
        logging.debug(str(tOrderList))
        
        tSave = False
        if tOrderList is not None:
            try:
                tOrder = tOrderList[0]
                tOrder.orderIsVerified = True
                tSave = True
            except:                
                if len(tOrderList) > 0:
                    tOrder = tOrderList
                    tOrder.orderIsVerified = True
                    tSave = True
                    
            if tSave:
                try:
                    tOrder.put()
                except:
                    pass
        