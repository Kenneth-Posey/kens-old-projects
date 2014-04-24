from models.customer import Customer
from models.customermaster import CustomerMaster
from google.appengine.ext import webapp
from models.order import Order
import logging, re
from google.appengine.api import taskqueue
from base import BaseHandler

class CustomerUpdate(webapp.RequestHandler):
    def get(self):
        return self.post()
    	
    def post(self):
        
        tOffset = str(self.request.get('offset'))

        if(tOffset == None or tOffset == ""):
            tOffset = 0
        else:	
            tOffset = int(tOffset)
        
        tUnattachedCustomer = Customer()
        
        tUnattachedCustomerQuery = Customer.all()
        tUnattachedCustomerQuery.filter("customerMaster !=", "")
        tUnattachedCustomerList = tUnattachedCustomerQuery.fetch(50, offset=tOffset)
        #logging.debug("Started with offset: " + str(tOffset))
        if(len(tUnattachedCustomerList) > 0):
            for tUnattachedCustomer in tUnattachedCustomerList: 
                tUnattachedCustomer.customerMaster = ""
                #logging.debug("Customer: " + str(tUnattachedCustomer.customerEmail))
                tUnattachedCustomer.put()
            
            tOffset = tOffset + 20
            taskqueue.add(url = '/customerupdate', countdown = 0, params = { 'offset' : str(tOffset)} )
        
        
class CustomerMasterHandler(BaseHandler):
    LOCATION = "../views/customermaster.html"
    def GetContext(self):
        tReturnDic = {}
        
        tMasterCustomerKey = str(self.request.get('key'))
        
        if( len(tMasterCustomerKey) > 0):
            try:
                tMasterCustomer = CustomerMaster.get(tMasterCustomerKey)
                
                if(str(tMasterCustomer.key()) > 0):
                    tReturnDic['mc'] = tMasterCustomer
                else:
                    tReturnDic['error'] = 'Master Customer Key Not Found'
            except:
                tReturnDic['error'] = 'Master Customer Key Not Found'
        else:
            tReturnDic['error'] = 'No Key Detected'
        
        return tReturnDic
        

class CustomerMasterUpdater(BaseHandler):
    LOCATION = "../views/customermaster.html"
    def get(self):
        tOrder = Order()
        tUnattachedCustomer = Customer()
        tMasterCustomer = CustomerMaster()
        tMasterCustomer.masterIsPaBlacklisted = False
        tMasterCustomer.masterIsGlobalBlacklisted = False
        
        #Lists of customer masters
        tMasterCustomerEmailList = []
        tMasterCustomerIpList = []
        tMasterCustomerPhoneList = []
        tMasterCustomerRsnList = []
        tMasterCustomerPaypalList = []
        
        tMasterCustomerEmailQuery = CustomerMaster.all()          
        tMasterCustomerIpQuery = CustomerMaster.all()    
        tMasterCustomerPhoneQuery = CustomerMaster.all()      
        tMasterCustomerRsnQuery = CustomerMaster.all()   
        tMasterCustomerPaypalQuery = CustomerMaster.all()
        
        #Final lists for deletion
        tDeletionList = []
        
        #First get an unmastered customer
        tUnattachedCustomerQuery = Customer.all()
        tUnattachedCustomerQuery.filter("customerMaster", "")
        #tUnattachedCustomerQuery.filter("customerEmail", "imma_gamer_pro@yahoo.com")
        tUnattachedCustomerList = tUnattachedCustomerQuery.fetch(1)
        if(len(tUnattachedCustomerList) > 0):
            tUnattachedCustomer = tUnattachedCustomerList[0]
        else:
            return
        
        #logging.debug("Testing with customer: " + str(tUnattachedCustomer.customerEmail))
        
        #Defaults
        tEmail = ""     
        tPhone = ""
        tIpList = []
        
        #Assign from unmastered customer
        tEmail = str(tUnattachedCustomer.customerEmail).strip().lower()
        tPhone = str(tUnattachedCustomer.customerPhone).strip().lower()
        tPhone = re.sub(r'\D', '', tPhone)
        
        for tIp in tUnattachedCustomer.customerIpAddresses:
            tIp = str(tIp).strip()
            if (tIp != '' and tIp != None):
                tIpList.append(tIp)
        
        #Get Customer's Orders
        tOrderQuery = Order.all()
        tOrderQuery.filter("orderPaypalEmail", tEmail)
        tOrderList = tOrderQuery.fetch(200)
        
        #Merge together a list of the RSNs and Order Paypal IDs
        tRsnList = []
        tPaypalList = []
        for tOrder in tOrderList:
            if(tOrder.orderAccountName != None and tOrder.orderAccountName != ""):
                tTempRsn = str(tOrder.orderAccountName).lower().strip()
                tTempRsn = tTempRsn.replace(' ', '_')
                tTempRsn = tTempRsn.replace('-', '_')
                tRsnList.append(tTempRsn)
            if(tOrder.orderCustomerPaypalId != None and tOrder.orderCustomerPaypalId != ""):
                tPaypalList.append(str(tOrder.orderCustomerPaypalId))

        #Dedupification
        tIpList = list(set(tIpList))
        tRsnList = list(set(tRsnList))
        tPaypalList = list(set(tPaypalList))
        
        #Now that the data to search is filled we can start searching for masters

        if(tEmail != None and tEmail != ""):
            #logging.debug("Searching for masters with customer email: " + str(tEmail))
            tMasterCustomerEmailQuery.filter("masterEmailList", tEmail)
            tMasterCustomerEmailList = tMasterCustomerEmailQuery.fetch(200)
            
        if(tPhone != None and tPhone != ""):
            #logging.debug("Searching for masters with customer phone: " + str(tPhone))
            tMasterCustomerPhoneQuery.filter("masterPhoneList", tPhone)
            tMasterCustomerPhoneList = tMasterCustomerPhoneQuery.fetch(200)
            
        if(len(tIpList) > 0):
            for tIp in tIpList:
                if(tIp != None and tIp != ""):
                    #logging.debug("Searching for masters with customer ip: " + str(tIp))        
                    tMasterCustomerIpQuery = CustomerMaster.all()    
                    tMasterCustomerIpQuery.filter("masterIpList", tIp)
                    tMasterCustomerIpList += tMasterCustomerIpQuery.fetch(200)
                
        if(len(tRsnList) > 0):
            for tRsn in tRsnList:
                if(tRsn != None and tRsn != ""):
                    #logging.debug("Searching for masters with customer rsn: " + str(tRsn))
                    tMasterCustomerRsnQuery = CustomerMaster.all()    
                    tMasterCustomerRsnQuery.filter("masterRsnList", tRsn)
                    tMasterCustomerRsnList += tMasterCustomerRsnQuery.fetch(200)
            
        if(len(tPaypalList) > 0):
            for tPaypal in tPaypalList:
                if(tPaypal != None and tPaypal != ""):
                    #logging.debug("Searching for masters with customer paypal id: " + str(tPaypal))
                    tMasterCustomerPaypalQuery = CustomerMaster.all()    
                    tMasterCustomerPaypalQuery.filter("masterPaypalIdList", tPaypal)
                    tMasterCustomerPaypalList += tMasterCustomerPaypalQuery.fetch(200)
            
        #logging.debug("Paypal Ids "+ str(tPaypalList))
        #logging.debug("")
            
        #Merge the lists together
        tMasterCustomerList = []
        tMasterCustomerList = tMasterCustomerEmailList + tMasterCustomerIpList + tMasterCustomerPaypalList + tMasterCustomerPhoneList + tMasterCustomerRsnList
        
        #if(len(tMasterCustomerEmailList) > 0):
            ##logging.debug("Master customer email list: " + str(tMasterCustomerEmailList))
            #tMasterCustomerList += tMasterCustomerEmailList
            
        #if(len(tMasterCustomerPhoneList) > 0):
            ##logging.debug("Master customer phone list: " + str(tMasterCustomerPhoneList))
            #tMasterCustomerList += tMasterCustomerPhoneList
            
        #if(len(tMasterCustomerIpList) > 0):
            ##logging.debug("Master customer ip list: " + str(tMasterCustomerIpList))
            #tMasterCustomerList += tMasterCustomerIpList
            
        #if(len(tMasterCustomerRsnList) > 0):
            ##logging.debug("Master customer rsn list: " + str(tMasterCustomerRsnList))
            #tMasterCustomerList += tMasterCustomerRsnList
            
        #if(len(tMasterCustomerPaypalList) > 0):
            ##logging.debug("Master customer paypalid list: " + str(tMasterCustomerPaypalList))
            #tMasterCustomerList += tMasterCustomerPaypalList
            
        #logging.debug("Number of Master Customers: " + str(len(tMasterCustomerList)))
        
        #ttMC = CustomerMaster()
        #for ttMC in tMasterCustomerList:
            #logging.debug("Master customer list item key: " + str(ttMC.key()))
        #logging.debug(str(tMasterCustomerList))
        
        #Assign or append lists of master customers
        if(len(tMasterCustomerList) > 1):
            tMC = CustomerMaster()
            tMcEmailList = []
            tMcPhoneList = []
            tMcIpList = []
            tMcRsnList = []
            tMcPaypalList = []
            tMcCustomerList = []
            
            for tMC in tMasterCustomerList:
                tMcEmailList += tMC.masterEmailList
                tMcPhoneList += tMC.masterPhoneList
                tMcIpList += tMC.masterIpList
                tMcRsnList += tMC.masterRsnList
                tMcPaypalList += tMC.masterPaypalIdList
                tMcCustomerList += tMC.masterCustomerList
                tDeletionList += [tMC]
            
            #for tMC in tMasterCustomerList:
                #if(len(tMC.masterEmailList) > 0):
                    #tMcEmailList += tMC.masterEmailList
                    ##tMcEmailList += tMasterCustomer.masterEmailList
                #if(len(tMC.masterPhoneList) > 0):
                    #tMcPhoneList += tMC.masterPhoneList
                    ##tMcPhoneList += tMasterCustomer.masterPhoneList
                #if(len(tMC.masterIpList) > 0):
                    #tMcIpList += tMC.masterIpList
                    ##tMcIpList += tMasterCustomer.masterIpList
                #if(len(tMC.masterRsnList) > 0):
                    #tMcRsnList += tMC.masterRsnList
                    ##tMcRsnList += tMasterCustomer.masterRsnList
                #if(len(tMC.masterPaypalIdList) > 0):
                    #tMcPaypalList += tMC.masterPaypalIdList
                    ##tMcPaypalList += tMasterCustomer.masterPaypalIdList
                #if(len(tMC.masterCustomerList) > 0):
                    #tMcCustomerList += tMC.masterCustomerList
                    ##tMcCustomerList += tMasterCustomer.masterCustomerList
                #tDeletionList += [tMC]
                
            tMcEmailList += [tEmail]
            tMcPhoneList += [tPhone]
            tMcIpList += tIpList
            tMcPaypalList += tPaypalList
            tMcRsnList += tRsnList
            tMcCustomerList += [str(tUnattachedCustomer.key())]
            
            tMasterCustomer.masterEmailList += list(set([str(x) for x in tMcEmailList if x != '' and x != None]))
            tMasterCustomer.masterPhoneList += list(set([str(x) for x in tMcPhoneList if x != '' and x != None]))
            tMasterCustomer.masterIpList += list(set([str(x).strip() for x in tMcIpList if x != '' and x != None]))
            tMasterCustomer.masterRsnList += list(set([str(x).strip().lower().replace('-','_').replace(' ','_') for x in tMcRsnList if x != '' and x != None]))
            tMasterCustomer.masterPaypalIdList += list(set([str(x) for x in tMcPaypalList if x != '' and x != None]))
            tMasterCustomer.masterCustomerList += list(set([str(x) for x in tMcCustomerList if x != '' and x != None]))
            
        ##############################################################################################################################################
        elif(len(tMasterCustomerList) == 1):
            tMC = tMasterCustomerList[0]
            #if(len(tMC.masterEmailList) > 0):
                #tMasterCustomer.masterEmailList += list(set([x for x in tMC.masterEmailList if x != '' and x != None]))
            #if(len(tMC.masterPhoneList) > 0):
                #tMasterCustomer.masterPhoneList += list(set([x for x in tMC.masterPhoneList if x != '' and x != None]))
            #if(len(tMC.masterIpList) > 0):
                #tMasterCustomer.masterIpList += list(set([x for x in tMC.masterIpList if x != '' and x != None]))
            #if(len(tMC.masterRsnList) > 0):
                #tMasterCustomer.masterRsnList += list(set([str(x).strip().lower().replace('-','_').replace(' ','_') for x in tMC.masterRsnList if x != '' and x != None]))
            #if(len(tMC.masterPaypalIdList) > 0):
                #tMasterCustomer.masterPaypalIdList += list(set([x for x in tMC.masterPaypalIdList if x != '' and x != None]))
            
            tMC.masterEmailList += [tEmail]
            tMC.masterIpList += tIpList
            tMC.masterPaypalIdList += tPaypalList
            tMC.masterPhoneList += [tPhone]
            tMC.masterRsnList += tRsnList
            
            tMasterCustomer.masterEmailList += list(set([x for x in tMC.masterEmailList if x != '' and x != None]))
            tMasterCustomer.masterPhoneList += list(set([x for x in tMC.masterPhoneList if x != '' and x != None]))
            tMasterCustomer.masterIpList += list(set([x for x in tMC.masterIpList if x != '' and x != None]))
            tMasterCustomer.masterRsnList += list(set([str(x).strip().lower().replace('-','_').replace(' ','_') for x in tMC.masterRsnList if x != '' and x != None]))
            tMasterCustomer.masterPaypalIdList += list(set([x for x in tMC.masterPaypalIdList if x != '' and x != None]))
            tMasterCustomer.masterCustomerList += [str(tUnattachedCustomer.key())]
            
            tDeletionList = [tMC]
        ##############################################################################################################################################
        elif(len(tMasterCustomerList) == 0):
            if(tMasterCustomer.masterCustomerList == None or len(tMasterCustomer.masterCustomerList) == 0):
                tTempList = []
                try:
                    tTempList.append(str(tUnattachedCustomer.key()))
                except:
                    tUnattachedCustomer.put()
                    tTempList.append(str(tUnattachedCustomer.key()))
                tMasterCustomer.masterCustomerList += tTempList
            if(tMasterCustomer.masterEmailList == None or len(tMasterCustomer.masterEmailList) == 0):
                tTempList = []
                tTempList.append(str(tUnattachedCustomer.customerEmail))
                tMasterCustomer.masterEmailList += tTempList
            if(tMasterCustomer.masterIpList == None or len(tMasterCustomer.masterIpList) == 0):
                tTempList = []
                tTempList += list(set(tUnattachedCustomer.customerIpAddresses))
                tMasterCustomer.masterIpList += tTempList
            if(tMasterCustomer.masterPaypalIdList == None or len(tMasterCustomer.masterPaypalIdList) == 0):
                tTempList = []
                tTempList.append(str(tUnattachedCustomer.customerPaypalId))
                tMasterCustomer.masterPaypalIdList += tTempList
            if(tMasterCustomer.masterPhoneList == None or len(tMasterCustomer.masterPhoneList) == 0):
                tTempList = []
                tTempList.append(str(tUnattachedCustomer.customerPhone))
                tMasterCustomer.masterPhoneList += tTempList
            if(tMasterCustomer.masterRsnList == None or len(tMasterCustomer.masterRsnList) == 0):
                tTempList = []
                tTempList += list(set(tRsnList))
                tMasterCustomer.masterRsnList += tTempList
        
        if(tUnattachedCustomer.customerIsPaBlacklisted == True):
            tMasterCustomer.masterIsPaBlacklisted = True
            
        if(tUnattachedCustomer.customerIsGlobalBlacklisted == True):
            tMasterCustomer.masterIsGlobalBlacklisted = True
    
        #for tProperty, tValue in tUnattachedCustomer.__dict__.iteritems():
            #logging.debug("Customer property " + str(tProperty) + " with value " + str(tValue))        
        
        #for tProperty, tValue in tMasterCustomer.__dict__.iteritems():
            #logging.debug("Master property " + str(tProperty) + " with value " + str(tValue))
        
        tMaster = CustomerMaster()       
        if(len(tDeletionList) > 0):
            for tMaster in tDeletionList:
                tMaster.delete()        
                
        tMasterKey = tMasterCustomer.put()
        
        #update other customers if there's >1
        tUnattachedCustomer.customerMaster = str(tMasterKey)
        tUnattachedCustomer.put()
        
        tCustomer = Customer()
        for tCustomerKey in tMasterCustomer.masterCustomerList:
            tCustomer = Customer.get(tCustomerKey)
            tCustomer.customerMaster = str(tMasterKey)
            tCustomer.put()
        
        #logging.debug("Master Key: " + str(tMasterKey))