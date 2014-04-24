
import StringIO
import webapp2, logging

from models.order import Order
from google.appengine.api import mail
from google.appengine.ext import db, webapp

from _stringmethods import StringMethods
from _numbertogp import NumberToGp

class EmailNotify(webapp2.RequestHandler):
    def post(self):
        
        tPaypalEmail = self.request.get('email')
        tCustomerName = self.request.get('name')
        tGoldAmount = self.request.get('gold')
        tOrderKey = self.request.get('key')
        
        tOrder = Order()
        tOrder = Order.get(tOrderKey)
        
        tVerificationCode = tOrder.orderVerificationCode
        
        tGoldInt = int(tGoldAmount.split('.')[0])
        logging.debug("Gold Int: " + str(tGoldInt))
        
        tGoldAmount = NumberToGp.ConvertIntToBet(tGoldInt)
        
        #logging.debug("Customer Name " + str(tCustomerName))
        #logging.debug("Gold Amount " + str(tGoldAmount))
        
        tMessage = """
        Dear %s,

        Thank you for choosing the eMeMO SmokinShop.
        
        We have received your payment for a code redeemable for %s. If you were not automatically returned to our website after payment, please go to http://smokinshop.com/delivery.php and speak to an eMeMO agent in the live chat.
        
        Your unique verification code is %s. You will also find your code attached to this email in a text file.
        
        Please speak to an eMeMO agent or visit http://smokinshop.com/delivery.php to activate your code and redeem it for RuneScape GP.
        
        Regards,
        
        The eMeMO Team
        """ % (str(tCustomerName), str(tGoldAmount), str(tVerificationCode)) 
                            
        logging.debug(str(tMessage))
        
        message         = mail.EmailMessage()
        message.sender  = "eMeMO SmokinShop Support<Support@eMeMO.com>"
        message.to      = tPaypalEmail
        message.subject = "eMeMO SmokinShop Order Details"
        message.body    = tMessage
        message.cc      = "support@ememo.com"
        message.attachments = [('verification-code.txt', tVerificationCode)]
        
        message.send()

class EmailChargeback(webapp.RequestHandler):
    def post(self):
        
        tPaypalEmail = self.request.get('email')
        #logging.debug("Chargeback Email for: " + tPaypalEmail)
        
        tMessage = """
        Dear Customer,
       
        It has come to our attention that you are attempting to reverse a payment you made via PayPal checkout on our website, http://smokinshop.com/goldshop.php. We would like to remind you that our Terms of Service state that payment reversals of any kind are not permitted for purchases made on our website due to the intangible nature of our product.  
        
        We sell game codes which can be exchanged for various goods for the game RuneScape. If you are reversing the payment because you do not recognize the charge then first check if a member of your household plays RuneScape as they may have made the payment without your permission, as is often the case. If the transaction was authorized then we recommend that you cancel the reversal to avoid a legal escalation of the matter.
        
        Yours faithfully,
        
        Kristijan Medic
        President & CEO
        Ememo INC
        kmedic@ememo.com


        Confidentiality Notice: This email and any attachments are eMeMO Confidential for the sole use of the intended recipient. Any review, copying, or distribution of this email and attachments by others is strictly prohibited. If you are not the intended recipient, please contact the sender immediately and permanently delete any copies of this email. 
        """
        
        #logging.debug(str(tMessage))
        
        mail.send_mail(sender = "eMeMO SmokinShop Support<Support@eMeMO.com>",
                       to = tPaypalEmail,
                       subject = "Recent Paypal Payment Reversal - IMPORTANT",
                       body = tMessage,
                       cc = "support@ememo.com")

        
        