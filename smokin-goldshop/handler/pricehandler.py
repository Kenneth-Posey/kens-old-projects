
import re, logging
from models.price import Price
from base import BaseHandler
import _data

class PriceHandler(BaseHandler):
    LOCATION = "../views/price.html"
    def GetContext(self):
        tContext = {}
        
        typeOfGold = self.GOLDTYPE
        
        tCurrentPrice = Price()
        tPriceQuery = Price().all()
        tPriceQuery.order("-priceDateCreated")
        tPriceQuery.filter("priceType", typeOfGold)
        tCurrentPrice = tPriceQuery.fetch(limit=1)[0]
            
        tPriceDictionary = _data.PriceContainer.GetBasePriceDictionary()
        
        typeOfGold = self.GOLDTYPE
        if typeOfGold is 'regular':
            tCurrentPrice.priceType = 'regular'
            tContext['post_location'] = '/price'
        elif typeOfGold is '07':
            tCurrentPrice.priceType = '07'
            tContext['post_location'] = '/price07'
        
        tSortedProperties = sorted(tCurrentPrice.properties().keys())
        for tCurrentProperty in tSortedProperties:
            try:
                tMatches = re.match(r'price(?P<number>[0-9]{4}m)', str(tCurrentProperty))
                tMatchedKey = str(tMatches.group('number'))
                
                tPriceDictionary[tMatchedKey] = tCurrentPrice.__getattribute__(tCurrentProperty)
            except:
                logging.debug('Could not find a key in: ' + str(tCurrentProperty))
        
        tPriceList = []
        tSortedPriceKeys = sorted(tPriceDictionary.keys())
        
        for tCurrentKey in tSortedPriceKeys:
            if(tCurrentKey[:3] == '000'):
                tKey = tCurrentKey[3:]
            elif(tCurrentKey[:2] == '00'):
                tKey = tCurrentKey[2:]
            elif(tCurrentKey[0] == '0'):
                tKey = tCurrentKey[1:]
            else:
                tKey = tCurrentKey
                
            tTuple = (tKey, tPriceDictionary[tCurrentKey])
            tPriceList.append(tTuple)
        
        #logging.debug(tPriceList)
        tContext['prices'] = tPriceList
        
        return tContext
        
            
    def PostContext(self):
        tContext = {}
        
        tPriceDictionary = _data.PriceContainer.GetBasePriceDictionaryWithoutZeros()
        
        tPriceList = []
        tSortedPriceKeys = sorted(tPriceDictionary.keys())
        
        for tCurrentKey in tSortedPriceKeys:
            if(len(tCurrentKey) == 2):
                tKey = "000" + tCurrentKey
            elif(len(tCurrentKey) == 3):
                tKey = "00" + tCurrentKey
            elif(len(tCurrentKey) == 4):
                tKey = "0" + tCurrentKey
            else:
                tKey = tCurrentKey
            #logging.debug('tCurrentKey ' + tCurrentKey)
            tTuple = (tKey, self.request.get(tCurrentKey))
            tPriceList.append(tTuple)
        #logging.debug('Price List construction complete')
        
        tCurrentPrice = Price()     
                
        typeOfGold = self.GOLDTYPE
        if typeOfGold is 'regular':
            tCurrentPrice.priceType = 'regular'
            self.LOCATION = '/price'
            tContext['post_location'] = '/price'
        elif typeOfGold is '07':
            tCurrentPrice.priceType = '07'
            self.LOCATION = '/price07'
            tContext['post_location'] = '/price07'
        
        #logging.debug(tPriceList)
        for tVolume, tNewPrice in tPriceList:
            #logging.debug("tVolume " + tVolume)
            #logging.debug("tNewPrice " + tNewPrice)
            tPropertyName = "price" + tVolume
            if tPropertyName in tCurrentPrice.properties().keys():
                try:
                    tCurrentPrice.__setattr__(tPropertyName, float(tNewPrice))
                except:
                    tCurrentPrice.__setattr__(tPropertyName, tNewPrice)
        
        #logging.debug("New price object constructed")
        #for tProperty in tCurrentPrice.properties().keys():
        #    logging.debug("Property " + tProperty + " is " + str(tCurrentPrice.properties()[tProperty]))
            
        tCurrentPrice.priceCreator = str(self.GetUser().email())
        
        #typeOfGold = self.request.get('goldtype')
        
        
        tCurrentPrice.put()
        
        self.REDIRECT = True
        
        return tContext