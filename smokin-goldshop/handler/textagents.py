import logging, urllib
from google.appengine.api import urlfetch
from baseajax import BaseAjax

class TextAgents(BaseAjax):
    def PostContext(self):
        tContext = {}
        tUserName = "REDACTED"
        tPass = "REDACTED"
        tUrl = "http://bulksms.vsms.net:5567/eapi/submission/send_sms/2/2.0"
        
        tMessage = "Agents are needed immediately in the goldshop. Please come online now if you are able."
        #tMessage = "This is a test of the offline goldshop agent notification system. Please post in the forum if you get this message."
        tPhoneList = [
                    '18434556817',  #courtland
                    '19253217648',  #ajay
                    '19092832433',  #dicingnigga
                    '18645411220',  #deox
                    '61468968175',  #epiqueness
                    '32492620585',  #divine
                    '447572122367', #tiggy
                    '14402213434',  #adrijana
                    '37063050140',  #dreamer
                    '447816169054', #mr j rune
                    '4795179994',   #shezzy
                    '14846436334',  #miken
                    '17788829733',  #wagerhost
                    '385977034860', #gskiki
                    '12093240084',  #i_pop_domez
                    #'15092207643', #kris/klippiii
                    #'18017182966', #frekwency
                    #'40728065418', #kitty meow
                    #'16784996457'  #mr pleco
                    ]
        
        for pPhone in tPhoneList:
            tPostPackage = {
                   'username' :  tUserName,
                   'password' :  tPass,
                   'message'  :  tMessage,
                   'msisdn'   :  pPhone
                }
            
            #logging.debug("Package " + str(tPostPackage))
            tPostPackage = urllib.urlencode(tPostPackage)
            tResponseText = urlfetch.fetch(url = tUrl, payload = tPostPackage, method = "POST", headers = {})
            if(tResponseText != None and tResponseText.content != None):
                tResponseText = tResponseText.content
            #logging.debug("Message for Phone: " + pPhone + " Response: " + tResponseText)
            
        #tResponse['tResponseText'] = "Success"
        self.response.out.write('Success')
        tContext['nowrite'] = True
        
        return tContext