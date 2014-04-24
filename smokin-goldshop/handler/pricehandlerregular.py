from pricehandler import PriceHandler

class PriceHandlerRegular(PriceHandler):
    def GetContext(self):
        self.GOLDTYPE = 'regular'
        return super(PriceHandlerRegular, self).GetContext()
    def PostContext(self):
        self.GOLDTYPE = 'regular'
        return super(PriceHandlerRegular, self).PostContext()