
import os, urllib, logging, datetime, re, ast

from _numbertogp import NumberToGp

from models.manualstockchange import ManualStockChange
from models.stocktransaction import StockTransaction
from models.stockaccount import StockAccount
from models.agent import Agent

from stockaccountmanager import StockAccountManager
from base import BaseHandler

class ManageCommission(BaseHandler):
    LOCATION = "../views/manage-commission.html"
    
    def GetContext(self):
        
        tStockAccount = StockAccount()
        tStockAccountManager = StockAccountManager()
        tStockAccountManager.LoadAccount('primary')
        tStockAccount = tStockAccountManager.CURRENT_STOCK
            
        return {
            'stock'     :   tStockAccount
        }   
        
    def PostContext(self):
        
        tStockAccount = StockAccount()
        tStockAccountManager = StockAccountManager()
        tStockAccountManager.LoadAccount('primary')
        tStockAccount = tStockAccountManager.CURRENT_STOCK
        
        t07Price = self.request.get('07price')
        tEocPrice = self.request.get('eocprice')
        
        if self.USER.email().lower() == 'corowns@gmail.com':        
            if t07Price is not None:
                if len(t07Price) > 0:
                    tStockAccount.stockPrice07 = float(t07Price)
                                    
            if tEocPrice is not None:
                if len(tEocPrice) > 0:
                    tStockAccount.stockPriceEoc = float(tEocPrice)        
        else:
            return {'error' : 'You bad bad boy. FBI Notified.'}
        
        tStockAccount.put()
        
        self.LOCATION = "/manage-commission"
        self.REDIRECT = True
        return {} #need to return something for processing
        #self.redirect(tLocation)
        
        
        