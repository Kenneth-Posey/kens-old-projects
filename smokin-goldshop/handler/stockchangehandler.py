
import os, urllib, logging, datetime, re, ast

from math import floor
from _numbertogp import NumberToGp

from models.manualstockchange import ManualStockChange
from models.stocktransaction import StockTransaction
from models.stockaccount import StockAccount
from models.agent import Agent

from stockaccountmanager import StockAccountManager
from base import BaseHandler

class StockChangeHandler(BaseHandler):
    LOCATION = "../views/manage-stock.html"
    REQUIRE_AUTH_POST = False
    
    def GetContext(self):
        
        tUser = self.GetUser()                
        tAllAgentList = []
        tAllStockList = []
        tTransactionList = []
        
        #tStock = ManualStockChange()
        #tAgent = Agent()
                
        tJulianStockAccount = StockAccount()
        tJulianManager = StockAccountManager()
        tJulianManager.LoadAccount('primary')
        tJulianStockAccount = tJulianManager.CURRENT_STOCK
        
        tCorownsStockAccount = StockAccount()
        tCorownsManager = StockAccountManager()
        tCorownsManager.LoadAccount('secondary')
        tCorownsStockAccount = tCorownsManager.CURRENT_STOCK
        
        tJulianEocStock = tJulianStockAccount.stockQuantityEoc / 1000
        tJulianEocStock = floor(tJulianEocStock)
        tJulianEocStock = int(tJulianEocStock) * 1000
        tTotalEoc = tJulianEocStock
        tJulianEocStock = NumberToGp.ConvertIntToBet(tJulianEocStock)
        
        tJulian07Stock = tJulianStockAccount.stockQuantity07 / 1000
        tJulian07Stock = floor(tJulian07Stock)
        tJulian07Stock = int(tJulian07Stock) * 1000
        tTotal07 = tJulian07Stock
        tJulian07Stock = NumberToGp.ConvertIntToBet(tJulian07Stock)
        
        tCorownsEocStock = tCorownsStockAccount.stockQuantityEoc / 1000
        tCorownsEocStock = floor(tCorownsEocStock)
        tCorownsEocStock = int(tCorownsEocStock) * 1000
        tTotalEoc = tTotalEoc + tCorownsEocStock
        tCorownsEocStock = NumberToGp.ConvertIntToBet(tCorownsEocStock)
        
        tCorowns07Stock = tCorownsStockAccount.stockQuantity07 / 1000
        tCorowns07Stock = floor(tCorowns07Stock)
        tCorowns07Stock = int(tCorowns07Stock) * 1000
        tTotal07 = tTotal07 + tCorowns07Stock
        tCorowns07Stock = NumberToGp.ConvertIntToBet(tCorowns07Stock)        
        
        #locale.setlocale(locale.LC_ALL, '')
        tOutstandingCommission = tJulianStockAccount.stockCommission
        tOutstandingCommission = round(tOutstandingCommission, 2)
        
        tOutstandingCommission = str(tOutstandingCommission)
        
        tNegative = False
        if tOutstandingCommission[0] == '-':
            tNegative = True
            tOutstandingCommission = tOutstandingCommission[1:]
        
        tRemainder = tOutstandingCommission.split('.')[1]
        if len(tRemainder) != 2:
            if len(tRemainder) == 1:
                tOutstandingCommission = tOutstandingCommission + '0'
            elif len(tRemainder) == 0:
                tOutstandingCommission = tOutstandingCommission + '00'
        
        if tNegative:
            tOutstandingCommission = '-$' + tOutstandingCommission
        else:
            tOutstandingCommission = '$' + tOutstandingCommission
        
        #tOutstandingCommission = locale.currency(tOutstandingCommission, grouping=True)
        
        tStringOffset = self.request.get('offset')
        if (len(tStringOffset) > 0):
            tOffset = int(tStringOffset)
        else:
            tOffset = 0
                       
        tNextIncrement = tOffset + 20
        if tOffset < 20:
            tPriorIncrement = 0
        else:
            tPriorIncrement = tOffset - 20            
        
        tDisplayForm = False
        if self.IsUserAdmin():
            tDisplayForm = True
        
        tTransQuery = StockTransaction.all()
        tTransQuery.order("-transDate")
        tTransactionList = tTransQuery.fetch(20, offset=tOffset)
        
        tTrans = StockTransaction()
        for tTrans in tTransactionList:
            tTrans.__dict__['transGoldAmountPretty'] = NumberToGp.ConvertIntToBet(tTrans.transGoldAmount)
            
        tTotal07 = NumberToGp.ConvertIntToBet(tTotal07)
        tTotalEoc = NumberToGp.ConvertIntToBet(tTotalEoc)
            
        return {
            'offset'       :   tOffset,
            'next'         :   tNextIncrement,
            'prev'         :   tPriorIncrement,
            'transactions' :   tTransactionList,
            'jeocstock'    :   tJulianEocStock,
            'j07stock'     :   tJulian07Stock,
            'ceocstock'    :   tCorownsEocStock,
            'c07stock'     :   tCorowns07Stock,
            'commission'   :   tOutstandingCommission,
            'displayform'  :   str(tDisplayForm),
            'total07'      :   tTotal07,
            'totaleoc'     :   tTotalEoc,
            #'stocklist' :   tAllStockList,
            #'agentlist' :   tAllAgentList
        }   
        
    def PostContext(self):
        
        logging.debug("request body {}".format(self.request.body))
        logging.debug("request body file {}".format(self.request.body_file))
        logging.debug("request address {}".format(self.request.remote_addr))
        logging.debug("request url {}".format(self.request.url))
        logging.debug("request query string {}".format(self.request.query_string))
        logging.debug("request headers {}".format(self.request.headers))
        logging.debug("request cookies {}".format(self.request.cookies))
        
        tDict = {}
        #logs the post data
        
        tDictString = str(self.request.body)
        try:
            #remove for hack
            #tBodyString = re.sub(r' \"amount":.*?,', '', str(tDictString))
            tDict = ast.literal_eval(tDictString)
            for key, value in tDict.items(): #turns json into dictionary
                logging.debug("argument: {} | value: {}".format(key, value))
            tWeb = False
        except:
            tWeb = True
        
        tAgent = Agent()
        tStockChange = ManualStockChange()
        tTransaction = StockTransaction()
        
        tJulianStockAccount = StockAccount()
        tJulianManager = StockAccountManager()
        tJulianManager.LoadAccount('primary')
        tJulianStockAccount = tJulianManager.CURRENT_STOCK
        
        tCorownsStockAccount = StockAccount()
        tCorownsManager = StockAccountManager()
        tCorownsManager.LoadAccount('secondary')
        tCorownsStockAccount = tCorownsManager.CURRENT_STOCK
        
        tTargetAccount = ''
        if tWeb: #is a web post not bot
            tAgent = str(self.request.get('agent')).lstrip().rstrip()
            tGoldType = str(self.request.get('goldtype')).lower().lstrip().rstrip()
            tComment = str(self.request.get('comment')).lstrip().rstrip()
            tReturn = bool(str(self.request.get('return')).lstrip().rstrip())
            tToken = str(self.request.get('token')).lstrip().rstrip()
            tGoldAmountWeb = str(self.request.get('amount')).lstrip().rstrip()     
            tTargetAccount = str(self.request.get('target')).lstrip().rstrip()
            
            if self.IsUserAdmin() != True:
                return {'error' : 'Only admins can modify stock' }
            
        else:
            tAgent = tDict['agent']
            tToken = tDict['token']
            tGoldType = tDict['goldtype']
            tGoldAmountWeb = str(tDict['amount'])
            #remove for hack
            #tGoldAmountPretty = re.compile(r'(([\-])*?\b[0-9]*.[0-9]*[kmb]{1}\b)').search(str(self.request.body)).groups()[0]    
                
            tComment = tDict['comment']
            tTargetAccount = "SMGamer"
            tReturn = False
                    
        if tToken != '9c8fcb2a-0bc2-4288-8880-0e2f3f42598d':
            return {}
            
        tGoldAmountPretty = re.sub(r'[^0-9kmb\-\.]*','', tGoldAmountWeb)
        tGoldMatches = re.match(r'([-]{1})?([0-9\.]*([kmb]{0,1}))', tGoldAmountPretty)
        if tGoldMatches is None:
            return {'error' : str(tGoldAmountPretty) + ' is an invalid gold amount'}
        
        #logging.debug('gold type ' + tGoldType)
        if (tGoldType in ('eoc', '07')) is not True:
            return {'error' : 'Invalid gold type' }
        
        tGoldAmount = NumberToGp.ConvertBetToInt(tGoldAmountPretty)
        
        #this is where stock is adjusted
        logging.debug("Stock adjustment debugging info")
        logging.debug("Is this a web request: {}".format(tWeb))
        logging.debug("Posted gold amount: {}".format(tGoldAmountWeb))
        logging.debug("Targetted account {}".format(tTargetAccount))
        logging.debug("Processed gold amount {}".format(tGoldAmount))
        if tWeb:
            if tTargetAccount == 'julian':
                tTransaction.transTarget = 'SMGamer'
                if tGoldType == 'eoc':
                    tJulianManager.SetEOCStock(int(tGoldAmount))                    
                else:
                    tJulianManager.Set07Stock(int(tGoldAmount))
                tJulianManager.AddCommission(int(tGoldAmount), tGoldType)
            elif tTargetAccount == 'corowns':
                tTransaction.transTarget = 'Goldshop'
                if tGoldType == 'eoc':
                    tCorownsManager.SetEOCStock(int(tGoldAmount))
                elif tGoldType == '07':
                    tCorownsManager.Set07Stock(int(tGoldAmount))
        else:
            if tGoldAmount < 0:
                if tGoldType == 'eoc':
                    if abs(tGoldAmount) < tJulianManager.GetCurrentEOCStock():
                        tJulianManager.SetEOCStock(int(tGoldAmount))
                    else:
                        tCorownsManager.SetEOCStock(int(tGoldAmount))                
                elif tGoldType == '07':
                    if abs(tGoldAmount) < tJulianManager.GetCurrent07Stock():
                        tJulianManager.Set07Stock(int(tGoldAmount))
                    else:
                        tCorownsManager.Set07Stock(int(tGoldAmount))
            else:
                if tGoldType == 'eoc':
                    tJulianManager.SetEOCStock(int(tGoldAmount))
                elif tGoldType == '07':
                    tJulianManager.Set07Stock(int(tGoldAmount))
                
            tJulianManager.AddCommission(int(tGoldAmount), tGoldType)
            tTransaction.transTarget = 'SMGamer'
            tComment = "BOT " + tComment
                 
        tStringOffset = self.request.get('offset')
        if (len(tStringOffset) > 0):
            tOffset = int(tStringOffset)
        else:
            tOffset = 0        
            
        if tAgent is '':
            tAgent = Agent()
            tAgent = Agent.GetAgentByEmail(self.USER.email())
            
            tAgent = tAgent.agentNickName
        
        tTransaction.transOwner = tAgent
        tTransaction.transGoldType = tGoldType
        tTransaction.transComment = tComment
        tTransaction.transGoldAmount = tGoldAmount
        tTransaction.transOwner = tAgent
        
        tTransactionGuid = tTransaction.put()
        
        if int(tOffset) > 0:
            self.LOCATION = '/stock?offset=' + str(tOffset)
        else:
            self.LOCATION = '/stock'
            
        self.REDIRECT = True
        return {} #need to return something for processing
        #self.redirect(tLocation)
        
        
        