# Main application file: "webapp/main.py"
    
import os, logging, locale, webapp2

from handler._numbertogp import NumberToGp

from public import mechanize    
from google.appengine.api import memcache, users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

from handler.about import AboutHandler

from models.agent import Agent 
from models.customer import Customer
from models.order import Order
from models.donorrecord import DonorRecord
from models.paorder import PaOrder

from handler.agentaccount import AgentAccount
from handler.agentgloballogout import AgentGlobalLogout
from handler.agenthandler import AgentHandler
from handler.agentlogging import AgentLogging
from handler.agenttimeout import AgentTimeout
from handler.agentmaster import AgentMaster
from handler.agentordernotification import AgentOrderNotification
from handler.base import BaseHandler
from handler.blacklist import Blacklist
from handler.customerhandler import CustomerHandler
from handler.customermasterhandler import CustomerMasterHandler, CustomerUpdate, CustomerMasterUpdater
from handler.iplookup import IpLookup
from handler.manualpaorder import ManualPaOrderHandler
from handler.phonelookup import PhoneLookup
#from handler.orderajax import OrderAjax, BlacklistAjax
from handler.ordergenerator import RandomOrderGenerator
from handler.orderhandler import OrderLookup, OrderHandler, DeliverOrder
from handler.pa import PASummary
from handler.paorder import PaOrderView
from handler.paorder import DeliverPaOrder
from handler.paypalipn import PaypalIpnHistory
from handler.paypalipndump import PaypalIpnDump
from handler.paypal import PaypalHandler, PaypalOrder
from handler.paypal import PaypalAgentTest, PaypalRefunds
#from handler.pricehandler import PriceHandler
from handler.pricehandler07 import PriceHandler07
from handler.pricehandlerregular import PriceHandlerRegular
from handler.pricejson import PriceJson
from handler.pricejson07 import PriceJson07
from handler.emailnotify import EmailNotify, EmailChargeback
from handler.referral import Referral, ReferralBalance, CalcReferral, AddReferralBonus
from handler.refundrollup import RefundRollup
from handler.stockchangehandler import StockChangeHandler
from handler.textagents import TextAgents
from handler.verifycode import VerifyCode
from handler.verifyemail import VerifyEmail
from handler.verifyid import VerifyId
from handler.verifyphone import VerifyPhone
from handler.vip import Vip
from handler.vipcancelpaypal import VipCancelPaypalAjax
from handler.vipcancelajax import VipCancel
from handler.vipcancellist import VipCancelList
from handler.viplist import VipList
from handler.viprefund import VipRefundPaypalAjax
from handler.vipsubscription import VipSubscription
from handler.vipupgradeajax import VipUpgradeAjax
from handler.vipupgradelist import VipUpgradeList
from handler.vipupgrademonitor import VipUpgradeMonitor
from handler.viprefund import VipRefundPaypalAjax
from handler.vipupgrademonitor import VipUpgradeScript
from handler._numbertogp import NumberToGp
from handler._stringmethods import StringMethods
from handler.managecommission import ManageCommission

from handler._tempscripts import ResetVip


class MainHandler(BaseHandler):
    LOCATION = "../views/index.html"
    
    def GetContext(self):
        tContext = {}
        tAgent = Agent()
        tAgentHandler = AgentHandler()
        tOrders = []
        tOrder = Order()
        tUser = self.USER
        
        tAgentQuery = Agent().all()
        tAgentQuery.filter('agentOnline', True)
        tAgents = tAgentQuery.fetch(100)
        if (len(tAgents) > 0):
            tContext['agentnum'] = len(tAgents)
            tContext['agents'] = tAgents
        try:
            tAgent = Agent().GetAgentByEmail(str(tUser.email()))
        except:
            pass
        if(tAgent.agentId == 'No Agent'):
            tAgent.agentCurrentCommission = 0.0
            tAgent.agentTotalCommission = 0.0
            tAgent.agentOrders = []
            tAgent.agentId = str(tUser.email())
            tAgent.agentGoldSupply = 0
            tAgent.agentOnline = False
            tAgent.put()
            
        if (tAgent.agentGoldSupply == None):
            tAgent.agentGoldSupply = 0
            
        tOrderQuery = PaOrder.all()
        tOrderQuery.filter("paDeliveryAgent", tAgent.agentId)
        tOrderQuery.order("-paDateDelivered")
        tOrdersRaw = tOrderQuery.fetch(50)
        
        tAgentDonorsQuery = DonorRecord.all()
        tAgentDonorsQuery.filter('donorAgent', tAgent.agentId)
        tAgentDonorsQuery.order('-donorDate')
        tAgentDonations = tAgentDonorsQuery.fetch(20)        
        
        for o in tOrdersRaw:
            tOrder = o
            if(tOrder != None):
                tOrders.append(tOrder)
        
        #tGoldSupply = tAgent.agentGoldSupply
        
        logging.debug('Original eoc ' + str(tAgent.agentGoldSupplyEoc))
        logging.debug('Original 07 ' + str(tAgent.agentGoldSupply07))
        
        tEocString = NumberToGp.ConvertIntToBet(tAgent.agentGoldSupplyEoc)
        t07String = NumberToGp.ConvertIntToBet(tAgent.agentGoldSupply07)
        
        logging.debug('Stringed version eoc ' + tEocString)
        logging.debug('Stringed version 07 ' + t07String)
        
        #tAgent.__setattr__('agentGoldSupplyEocString', tEocString)
        #tAgent.__setattr__('agentGoldSupply07String', t07String)
        
        
        tContext['agent'] = tAgent
        tContext['gpeocstring'] = str(tEocString)
        tContext['gp07string'] = str(t07String)
        #tContext['agentgold'] = locale.format("%d", int(tGoldSupply), grouping = True)
        tContext['orders'] = tOrders
        tContext['agentcomm'] = locale.format("%0.2f", tAgent.agentCurrentCommission, grouping = True)
        tContext['agenttotal'] = locale.format("%0.2f", tAgent.agentTotalCommission, grouping = True)
        tContext['donations'] = tAgentDonations
        return tContext
    
    def PostContext(self):
        tContext = {}
        tAgent = Agent()

        tUser = self.GetUser()
        tAgent = Agent.GetAgentByEmail(tUser.email())
        tSaveAgent = False
        tNewNick = self.request.get('nick')
        tSoundOpt = self.request.get('sound')
        
        if(tNewNick != None and len(tNewNick) > 0):
            tAgent.agentNickName = tNewNick
            tSaveAgent = True
            
        if(tSoundOpt != None and len(tSoundOpt) > 0):
            tSoundOpt = str(tSoundOpt)
            if(tSoundOpt == "true"):
                tAgent.agentSoundPreference = 'True'
                tSaveAgent = True
            elif(tSoundOpt == "false"):
                tAgent.agentSoundPreference = 'False'
                tSaveAgent = True
                
        if(tSaveAgent):
            tAgent.put()
        self.LOCATION = "/"
        self.REDIRECT = True
        return tContext
        
    
tUrlHandlers = [('/', MainHandler),
                ('/addreferralbonus', AddReferralBonus),
                ('/agent', AgentHandler),
                ('/agentaccount', AgentAccount),
                ('/agentmaster', AgentMaster),
                ('/agentout', AgentTimeout),
                ('/allout', AgentGlobalLogout),
                ('/blacklist', Blacklist),
                ('/calcreferral',CalcReferral),
                ('/completeorder', DeliverOrder),
                ('/customerlookup', CustomerHandler),
                ('/customermaster', CustomerMasterHandler),
                ('/customermasterupdate', CustomerMasterUpdater),
                ('/customerupdate', CustomerUpdate),
                ('/emailnotify', EmailNotify),
                ('/emailchargeback', EmailChargeback),
                ('/iplookup', IpLookup),
                ('/ipnhistory', PaypalIpnHistory),
                ('/log', AgentLogging),
                ('/manage-commission', ManageCommission),
                ('/notify', AgentOrderNotification),
                ('/order', OrderHandler),
                ('/ordergen', RandomOrderGenerator),
                ('/orderlookup', OrderLookup),
                ('/pa', PASummary),
                ('/palist', ManualPaOrderHandler),
                ('/paorder', PaOrderView),
                ('/paorderdeliver', DeliverPaOrder),
                ('/paypal', PaypalHandler),
                ('/paypalagenttest', PaypalAgentTest),
                ('/paypalipn', PaypalOrder),
                ('/paypalipndump', PaypalIpnDump),
                ('/paypalorder', PaypalOrder),
                #('/price', PriceHandler),
                ('/price', PriceHandlerRegular),
                ('/price07', PriceHandler07),
                ('/pricejson', PriceJson),
                ('/pricejson07', PriceJson07),
                ('/phonelookup', PhoneLookup),
                ('/referral', Referral),
                ('/referralbalance', ReferralBalance),
                ('/refund', PaypalRefunds),
                ('/refundrollup', RefundRollup),
                ('/stock', StockChangeHandler),
                ('/stockREMOVEME', StockChangeHandler),
                ('/textagents', TextAgents),
                ('/verify-code', VerifyCode),
                ('/verifyemail', VerifyEmail),
                ('/verifyphone', VerifyPhone),
                ('/verifyid', VerifyId),
                ('/vip', Vip),
                ('/viplist', VipList),
                ('/vipcancel', VipCancel),
                ('/vipcancellist', VipCancelList),
                ('/vipcancelpaypal', VipCancelPaypalAjax),
                ('/viprefund', VipRefundPaypalAjax),
                ('/vipsubscription', VipSubscription),
                ('/vipupgrade', VipUpgradeAjax),
                ('/vipupgradelist', VipUpgradeList),
                ('/vipupgrademonitor', VipUpgradeMonitor)
                ]

application = webapp2.WSGIApplication(tUrlHandlers, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()