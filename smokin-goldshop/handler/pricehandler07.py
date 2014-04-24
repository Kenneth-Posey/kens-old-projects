from pricehandler import PriceHandler

class PriceHandler07(PriceHandler):    
    def GetContext(self):
        self.GOLDTYPE = '07'
        return super(PriceHandler07, self).GetContext()
    def PostContext(self):
        self.GOLDTYPE = '07'
        return super(PriceHandler07, self).PostContext()