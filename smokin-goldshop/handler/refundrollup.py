from models.order import Order
from base import BaseHandler

class RefundRollup(BaseHandler):
    LOCATION = '../views/refundrollup.html'
    def GetContext(self):
        tContext = {}
        tOrderQuery = Order.all()
        tOrderQuery.filter("orderDeliver", "False")
        tOrderQuery.order("orderCreated")
        tOrderList = tOrderQuery.fetch(500)
        tContext['orders'] = tOrderList
        
        return tContext