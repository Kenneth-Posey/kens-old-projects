import os, urllib, logging, datetime, re

from _numbertogp import NumberToGp

from stockaccountmanager import StockAccountManager

from models.manualstockchange import ManualStockChange
from models.stockaccount import StockAccount
from models.agent import Agent

from base import BaseHandler

class StockManager(object):
    JULIAN_STOCK = StockAccountManager()
    COROWNS_STOCK = StockAccountManager()
        
    def LoadAccounts(self):
        tCorownsAccount = StockAccountManager()
        tJulianAccount = StockAccountManager()
        
        tCorownsAccount.LoadAccount('secondary')
        tJulianAccount.LoadAccount('primary')
        
        self.JULIAN_STOCK = tJulianAccount
        self.COROWNS_STOCK = tCorownsAccount
        
    # commission is calced on the order processor
    def PlaceOrder(self, aGoldQuantity, aGoldType):
        
        logging.debug("{}".format(aGoldQuantity))
        logging.debug("{}".format(aGoldType))
        logging.debug("{}".format(self.COROWNS_STOCK.GetCurrent07Stock()))
        logging.debug("{}".format(self.COROWNS_STOCK.GetCurrentEOCStock()))
        logging.debug("{}".format(self.JULIAN_STOCK.GetCurrent07Stock()))
        logging.debug("{}".format(self.JULIAN_STOCK.GetCurrentEOCStock()))
        
        if aGoldQuantity < 0:
            aGoldQuantity = aGoldQuantity * -1
        
        if aGoldType == 'eoc':
            if aGoldQuantity < self.COROWNS_STOCK.GetCurrentEOCStock():
                logging.debug("removing from corowns")
                self.COROWNS_STOCK.SetEOCStock(int(aGoldQuantity * -1))
            elif aGoldQuantity < self.JULIAN_STOCK.GetCurrentEOCStock():
                logging.debug("removing from julian")
                self.JULIAN_STOCK.SetEOCStock(int(aGoldQuantity * -1))
            else:
                raise Exception("No EOC stock left")
        elif aGoldType == '07':
            if aGoldQuantity < self.COROWNS_STOCK.GetCurrent07Stock():
                logging.debug("removing from corowns")
                self.COROWNS_STOCK.Set07Stock(int(aGoldQuantity * -1))
            elif aGoldQuantity < self.JULIAN_STOCK.GetCurrent07Stock():
                logging.debug("removing from julian")
                self.JULIAN_STOCK.Set07Stock(int(aGoldQuantity * -1))
            else:
                raise Exception("No 07 stock left")
            
    # negative stock change => negative commission
    def ManualStockChange(self, aGoldQuantity, aGoldType, aTargetAccount):
        
        tIsNegative = aGoldQuantity <= 0
        
        if aTargetAccount == 'julian':
            if aGoldType == 'eoc':        
                #tNewStock = self.JULIAN_STOCK.CURRENT_STOCK.stockQuantityEoc + aGoldQuantity
                self.JULIAN_STOCK.SetEOCStock(aGoldQuantity)
                self.JULIAN_STOCK.AddCommission(aGoldQuantity, aGoldType)
            elif aGoldType == '07':
                #tNewStock = self.JULIAN_STOCK.CURRENT_STOCK.stockQuantity07 + aGoldQuantity
                self.JULIAN_STOCK.Set07Stock(aGoldQuantity)
                self.JULIAN_STOCK.AddCommission(aGoldQuantity, aGoldType)
        elif aTargetAccount == 'corowns':
            if aGoldType == 'eoc':        
                #tNewStock = self.COROWNS_STOCK.CURRENT_STOCK.stockQuantityEoc + aGoldQuantity
                self.COROWNS_STOCK.SetEOCStock(aGoldQuantity)
            elif aGoldType == '07':
                #tNewStock = self.COROWNS_STOCK.CURRENT_STOCK.stockQuantity07 + aGoldQuantity
                self.COROWNS_STOCK.Set07Stock(aGoldQuantity)