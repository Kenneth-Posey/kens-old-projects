import os, urllib, logging, datetime, re

from _numbertogp import NumberToGp

from stockaccountmanager import StockAccountManager

from models.manualstockchange import ManualStockChange
from models.stockaccount import StockAccount
from models.agent import Agent

from base import BaseHandler

class CommissionManager(object):
    JULIAN_STOCK = StockAccountManager()
    COROWNS_STOCK = StockAccountManager()
        
    def LoadAccounts(self):
        tCorownsAccount = StockAccountManager()
        tJulianAccount = StockAccountManager()
        
        tCorownsAccount.LoadAccount('secondary')
        tJulianAccount.LoadAccount('primary')
        
        self.JULIAN_STOCK = tJulianAccount
        self.COROWNS_STOCK = tCorownsAccount