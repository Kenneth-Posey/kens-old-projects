import os, urllib, logging, datetime, re

from _numbertogp import NumberToGp

from models.manualstockchange import ManualStockChange
from models.agent import Agent
from models.stockaccount import StockAccount
from base import BaseHandler

class StockAccountManager(object):
    CURRENT_STOCK = StockAccount()
    CURRENT_EOC = float()
    CURRENT_07 = float()
    
    def LoadAccount(self, aAccountName):
        tStockAccount = StockAccount()
        
        tStockQuery = StockAccount.all()
        tStockQuery.filter('stockName', aAccountName)
        tStockAccount = tStockQuery.fetch(limit = 1)
        tStockAccount = tStockAccount[0]
        
        self.CURRENT_STOCK = tStockAccount
        self.CURRENT_07 = tStockAccount.stockPrice07
        self.CURRENT_EOC = tStockAccount.stockPriceEoc
        
        return self.CURRENT_STOCK.key()
            
    def GetCurrentEOCStock(self):
        return self.CURRENT_STOCK.stockQuantityEoc
    
    def GetCurrent07Stock(self):
        return self.CURRENT_STOCK.stockQuantity07
        
    def SetEOCStock(self, aNewStockAmount):                
        return self.SetStock(aNewStockAmount, 'eoc',)
        
    def Set07Stock(self, aNewStockAmount):     
        return self.SetStock(aNewStockAmount, '07',)
        
    def SetStock(self, aNewStockAmount, aGoldType):
        tStockAccount = StockAccount()        
        tStockAccount = self.CURRENT_STOCK       
        #logging.debug("{}".format(aNewStockAmount))
        #logging.debug("{}".format(aGoldType))
        if aGoldType == "07":
            tStockAccount.stockQuantity07 = tStockAccount.stockQuantity07 + aNewStockAmount
        elif aGoldType == "eoc":
            tStockAccount.stockQuantityEoc = tStockAccount.stockQuantityEoc + aNewStockAmount
            
        tKey = tStockAccount.put()        
        self.CURRENT_STOCK = tStockAccount
        
        return tKey
    
    def AddCommission(self, aGoldAmount, aGoldType):
        tStockAccount = StockAccount()
        
        tStockAccount = self.CURRENT_STOCK       
        
        if aGoldType == "07":
            tCommission = aGoldAmount * self.CURRENT_07 / 1000000
            
        elif aGoldType == "eoc":
            tCommission = aGoldAmount * self.CURRENT_EOC / 1000000
            
        tStockAccount.stockCommission = tStockAccount.stockCommission + tCommission
            
        tKey = tStockAccount.put()        
        self.CURRENT_STOCK = tStockAccount
        
        return tKey        