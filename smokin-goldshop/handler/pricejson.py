import re, logging, json, webapp2
from models.price import Price
from _data import PriceContainer

class PriceJson(webapp2.RequestHandler):
    def get(self):
        tCurrentPrices = PriceContainer.GetCurrentPriceDic()
        if(self.request.get('simple') == 'True'):
            tSimplePrices = {}
            for tKey in tCurrentPrices.keys():
                if 'm' in tKey:
                    tSimplePrices[tKey] = tCurrentPrices[tKey]
                    
            self.response.out.write(json.dumps(tSimplePrices))
        else:
            self.response.out.write(json.dumps(tCurrentPrices))

