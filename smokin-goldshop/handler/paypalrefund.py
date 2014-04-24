
import urllib
from google.appengine.ext import webapp
from public import mechanize

class PaypalRefund(webapp.RequestHandler):
    
    #Modified for account security
    API_PASSWORD  = "REDACTED"
    API_USERNAME  = "REDACTED"
    API_SIGNATURE = "REDACTED"
    
    def post(self):
        tUrl = "https://api-3t.paypal.com/nvp"
        tOperation = "GetTransactionDetails"
        tPaypal = PaypalRefund()
        tResultDictionary = {}
        tPaypalPayload = {}        
        tPayload = {}
        
        #logging.debug("Transaction id: " + str(self.request.get('transactionid')))
        #logging.debug("Gold amount: " + str(self.request.get('gold')))
        #logging.debug("Name: " + str(self.request.get('name')))
        #logging.debug("Email: " + str(self.request.get('email')))
        #logging.debug("Mobile" + str(self.request.get('mobile')))
        #logging.debug("RS Name: " + str(self.request.get('rsname')))
        #logging.debug("Combat: " + str(self.request.get('cblvl')))
        #logging.debug("Promocode: " + str(self.request.get('promotion')))
        #logging.debug("Ip: " + str(self.request.get('customerip')))
        
        tPaypalPayload['METHOD'] = tOperation
        tPaypalPayload['TRANSACTIONID'] = str(self.request.get('transactionid'))
        
        tPayloadEncoded = tPaypal.GeneratePayload(tPaypalPayload)
        
        request_cookies = mechanize.CookieJar()
        request_opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(request_cookies))
        request_opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
        mechanize.install_opener(request_opener)
            
        tResponse = mechanize.urlopen(url = tUrl, timeout = 25.0, data = tPayloadEncoded)
        tResult = str(urllib.unquote(tResponse.read()))
        
        #logging.debug("Mechanize Package")
        #logging.debug("Url: " + tUrl)
        #logging.debug("Data: " + str(tPaypalPayload))
        #logging.debug("Response: " + tResult)
        
        tResultSplit = tResult.split('&')
        
        for tPair in tResultSplit:
            tSplitPair = tPair.split("=")
            tResultDictionary[tSplitPair[0]] = tSplitPair[1]

            
    
    def GeneratePayload(self, pPayload):
        tPayload = {}
        tPayload = pPayload
        tBasePayload = {
            "USER" : self.API_USERNAME,
            "PWD" : self.API_PASSWORD,
            "SIGNATURE" : self.API_SIGNATURE,
            "VERSION" : "72.0"
            }
        
        for tKey in tPayload.keys():
            tBasePayload[tKey] = tPayload[tKey]
        
        return urllib.urlencode(tBasePayload)