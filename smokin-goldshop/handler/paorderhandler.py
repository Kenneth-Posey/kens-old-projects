import logging, email, types, base64, re
from _numbertogp import NumberToGp
from deliveryassignment import DeliveryAssignment
from models.paorder import PaOrder
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 


class PaOrderHandler(InboundMailHandler):
    
    reUtfStripper = re.compile("=\?utf-8\?B\?(?P<text>.*)\?=")
    reOrder = re.compile("Order: (?P<order>.*) r")
    reOrderId = re.compile("Order ID: (?P<orderid>.*) *")
    
    def receive(self, mail_message):
        #logging.debug("Received a message from: " + PaOrderHandler.unwraptext(mail_message.sender))
        #logging.debug("Subject: " + PaOrderHandler.unwraptext(mail_message.subject))

        for bodies in mail_message.bodies('text/plain'):
            emailtext = ""
            for body in bodies:
                try:
                    encodedtext = body[1]
                    emailtext = PaOrderHandler.unwraptext(encodedtext)
                except:
                    emailtext = body.payload.decode(body.encoding)
                    
                if(isinstance(emailtext, unicode)):
                    emailtext = emailtext.encode('utf-8')
                
            #logging.debug("Body PlainText: " + emailtext)
            
        OrderAmountText = self.reOrder.search(emailtext).groupdict()['order'].strip()
        OrderAmountInt = NumberToGp.ConvertBetToInt(OrderAmountText)
        OrderId = self.reOrderId.search(emailtext).groupdict()['orderid'].strip()
        
        tMatchingOrderQuery = PaOrder.all()
        tMatchingOrderQuery.filter("paTransactionId", OrderId)
        
        tMatches = tMatchingOrderQuery.fetch(10)
        
        if(len(tMatches) > 0):
            return
        
        tPaOrder = PaOrder()
        tPaOrder.paAmount = OrderAmountText
        tPaOrder.paAmountInt = OrderAmountInt
        tPaOrder.paTransactionId = OrderId

        tAssignedAgentClass = DeliveryAssignment() 
        tAssignedAgent = tAssignedAgentClass.GetAssignedAgent()
        
        if(tAssignedAgent != 'No Agent Online'):
            tPaOrder.paAssignedAgent = tAssignedAgent.agentId
            tPaOrder.paAssignedAgentNick = tAssignedAgent.agentNickName
        else:
            tPaOrder.paAssignedAgent = "No Agent Online"
            tPaOrder.paAssignedAgentNick = "No Agent Online"
            
        tPaOrder.put()
        
    @staticmethod
    def unwraptext(encodedtext):
        #logging.debug("Encoded text: " + encodedtext)

        try:
            encodedtext = self.reUtfStripper.search(encodedtext).groupdict()['text']
    
            modvalue = len(encodedtext) % 4                
            if(modvalue != 0):
                remainder = 4 - modvalue
                while(remainder > 0):
                    encodedtext += "="
                    remainder -= 1
                
            return base64.b64decode(encodedtext)
        except:
            return encodedtext