
import os, logging, random, urllib
from customerhandler import CustomerHandler
from models.customer import Customer
from google.appengine.api import memcache, users, urlfetch
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

class VerifyPhone(webapp.RequestHandler):
    def post(self):
        pPhone = str(self.request.get('phone'))
        pCustomerId = self.request.get('custid')
        pMarkVerified = self.request.get('verified')
        tUserName = "Ememo"
        tPass = "Plecoftw1"
        tUrl = "http://usa.bulksms.com:5567/eapi/submission/send_sms/2/2.0"
        
        tCustomer = Customer.get(pCustomerId)
        tNumber = random.randint(200, 999)
        
        if(pMarkVerified != None and pMarkVerified == 'True'):
            tCustomer.customerPhoneVerified = True                    
            tCustomer.put()
            
            self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
            self.response.headers['Content-Type'] = 'Content-Type: plain/text'
            self.response.out.write("Verified")

        else:
            tMessage = "Verification Number: " + str(tNumber)
            tPostPackage = {
                   'username'      :   tUserName,
                   'password'      :   tPass,
                   'message'    :   tMessage,
                   'msisdn'   : pPhone
                }
            #logging.debug("Package " + str(tPostPackage))
            tPostPackage = urllib.urlencode(tPostPackage)
            tResponse = urlfetch.fetch(url = tUrl, payload = tPostPackage, method = "POST", headers = {})
            tResponse = tResponse.content
            #logging.debug("Message for Phone: " + pPhone + " Response: " + tResponse)
            tCustomer.customerPhoneVerificationNumber = str(tNumber)
                
            tCustomer.put()
            
            self.response.headers['Cache-Control'] = 'Cache-Control: no-cache, must-revalidate'
            self.response.headers['Content-Type'] = 'Content-Type: plain/text'
            self.response.out.write("New: " + str(tNumber))
            
            
    def PopulateCodeList(self):
        tMatchString = "<a href=\"([a-zA-Z_ ]*)\">(?P<country>(.*?))</a>(.*?)<td align=\"center\">(.*?)</td>(.*?)<td align=\"center\">(?P<code>[0-9 ]*)&nbsp;</td>"
        tMatch = re.compile(tMatchString, re.DOTALL)
        tMatchList = tMatch.findall(tContent)
        tMatchList = [('Afghanistan', '93'), ('Albania', '355'), ('Algeria', '213'), ('American Samoa', '1 684'), 
                      ('Andorra', '376'), ('Angola', '244'), ('Anguilla', '1 264'), ('Antarctica', '672'), 
                      ('Antigua and Barbuda', '1 268'), ('Argentina', '54'), ('Armenia', '374'), ('Aruba', '297'), 
                      ('Australia', '61'), ('Austria', '43'), ('Azerbaijan', '994'), ('Bahamas', '1 242'), 
                      ('Bahrain', '973'), ('Bangladesh', '880'), ('Barbados', '1 246'), ('Belarus', '375'), 
                      ('Belgium', '32'), ('Belize', '501'), ('Benin', '229'), ('Bermuda', '1 441'), ('Bhutan', '975'), 
                      ('Bolivia', '591'), ('Bosnia and Herzegovina', '387'), ('Botswana', '267'), ('Brazil', '55'), 
                      ('British Indian Ocean Territory', ''), ('British Virgin Islands', '1 284'), ('Brunei', '673'), 
                      ('Bulgaria', '359'), ('Burkina Faso', '226'), ('Burma (Myanmar)', '95'), ('Burundi', '257'), 
                      ('Cambodia', '855'), ('Cameroon', '237'), ('Canada', '1'), ('Cape Verde', '238'), 
                      ('Cayman Islands', '1 345'), ('Central African Republic', '236'), ('Chad', '235'), 
                      ('Chile', '56'), ('China', '86'), ('Christmas Island', '61'), ('Cocos (Keeling) Islands', '61'), 
                      ('Colombia', '57'), ('Comoros', '269'), ('Republic of the Congo', '242'), 
                      ('Democratic Republic of the Congo', '243'), ('Cook Islands', '682'), ('Costa Rica', '506'), 
                      ('Croatia', '385'), ('Cuba', '53'), ('Cyprus', '357'), ('Czech Republic', '420'), ('Denmark', '45'),
                      ('Djibouti', '253'), ('Dominica', '1 767'), ('Dominican Republic', '1 809'), ('Timor-Leste', '670'),
                      ('Ecuador', '593'), ('Egypt', '20'), ('El Salvador', '503'), ('Equatorial Guinea', '240'), 
                      ('Eritrea', '291'), ('Estonia', '372'), ('Ethiopia', '251'), ('Falkland Islands', '500'), 
                      ('Faroe Islands', '298'), ('Fiji', '679'), ('Finland', '358'), ('France', '33'), 
                      ('French Polynesia', '689'), ('Gabon', '241'), ('Gambia', '220'), ('Gaza Strip', '970'), 
                      ('Georgia', '995'), ('Germany', '49'), ('Ghana', '233'), ('Gibraltar', '350'), ('Greece', '30'), 
                      ('Greenland', '299'), ('Grenada', '1 473'), ('Guam', '1 671'), ('Guatemala', '502'), 
                      ('Guinea', '224'), ('Guinea-Bissau', '245'), ('Guyana', '592'), ('Haiti', '509'), 
                      ('Honduras', '504'), ('Hong Kong', '852'), ('Hungary', '36'), ('Iceland', '354'), ('India', '91'), 
                      ('Indonesia', '62'), ('Iran', '98'), ('Iraq', '964'), ('Ireland', '353'), ('Isle of Man', '44'), 
                      ('Israel', '972'), ('Italy', '39'), ('Ivory Coast', '225'), ('Jamaica', '1 876'), ('Japan', '81'), 
                      ('Jersey', ''), ('Jordan', '962'), ('Kazakhstan', '7'), ('Kenya', '254'), ('Kiribati', '686'), 
                      ('Kosovo', '381'), ('Kuwait', '965'), ('Kyrgyzstan', '996'), ('Laos', '856'), ('Latvia', '371'), 
                      ('Lebanon', '961'), ('Lesotho', '266'), ('Liberia', '231'), ('Libya', '218'), 
                      ('Liechtenstein', '423'), ('Lithuania', '370'), ('Luxembourg', '352'), ('Macau', '853'), 
                      ('Macedonia', '389'), ('Madagascar', '261'), ('Malawi', '265'), ('Malaysia', '60'), 
                      ('Maldives', '960'), ('Mali', '223'), ('Malta', '356'), ('Marshall Islands', '692'), 
                      ('Mauritania', '222'), ('Mauritius', '230'), ('Mayotte', '262'), ('Mexico', '52'), 
                      ('Micronesia', '691'), ('Moldova', '373'), ('Monaco', '377'), ('Mongolia', '976'), 
                      ('Montenegro', '382'), ('Montserrat', '1 664'), ('Morocco', '212'), ('Mozambique', '258'), 
                      ('Namibia', '264'), ('Nauru', '674'), ('Nepal', '977'), ('Netherlands', '31'), 
                      ('Netherlands Antilles', '599'), ('New Caledonia', '687'), ('New Zealand', '64'), 
                      ('Nicaragua', '505'), ('Niger', '227'), ('Nigeria', '234'), ('Niue', '683'), 
                      ('Norfolk Island', '672'), ('Northern Mariana Islands', '1 670'), ('North Korea', '850'), 
                      ('Norway', '47'), ('Oman', '968'), ('Pakistan', '92'), ('Palau', '680'), ('Panama', '507'), 
                      ('Papua New Guinea', '675'), ('Paraguay', '595'), ('Peru', '51'), ('Philippines', '63'), 
                      ('Pitcairn Islands', '870'), ('Poland', '48'), ('Portugal', '351'), ('Puerto Rico', '1'), 
                      ('Qatar', '974'), ('Romania', '40'), ('Russia', '7'), ('Rwanda', '250'), ('Saint Barthelemy', '590'), 
                      ('Samoa', '685'), ('San Marino', '378'), ('Sao Tome and Principe', '239'), ('Saudi Arabia', '966'), 
                      ('Senegal', '221'), ('Serbia', '381'), ('Seychelles', '248'), ('Sierra Leone', '232'), 
                      ('Singapore', '65'), ('Slovakia', '421'), ('Slovenia', '386'), ('Solomon Islands', '677'), 
                      ('Somalia', '252'), ('South Africa', '27'), ('South Korea', '82'), ('Spain', '34'), 
                      ('Sri Lanka', '94'), ('Saint Helena', '290'), ('Saint Kitts and Nevis', '1 869'), 
                      ('Saint Lucia', '1 758'), ('Saint Martin', '1 599'), ('Saint Pierre and Miquelon', '508'), 
                      ('Saint Vincent and the Grenadines', '1 784'), ('Sudan', '249'), ('Suriname', '597'), 
                      ('Svalbard', ''), ('Swaziland', '268'), ('Sweden', '46'), ('Switzerland', '41'), ('Syria', '963'), 
                      ('Taiwan', '886'), ('Tajikistan', '992'), ('Tanzania', '255'), ('Thailand', '66'), ('Togo', '228'),
                      ('Tokelau', '690'), ('Tonga', '676'), ('Trinidad and Tobago', '1 868'), ('Tunisia', '216'), 
                      ('Turkey', '90'), ('Turkmenistan', '993'), ('Turks and Caicos Islands', '1 649'), ('Tuvalu', '688'),
                      ('United Arab Emirates', '971'), ('Uganda', '256'), ('United Kingdom', '44'), ('Ukraine', '380'), 
                      ('Uruguay', '598'), ('United States', '1'), ('Uzbekistan', '998'), ('Vanuatu', '678'), 
                      ('Holy See (Vatican City)', '39'), ('Venezuela', '58'), ('Vietnam', '84'), 
                      ('US Virgin Islands', '1 340'), ('Wallis and Futuna', '681'), ('West Bank', '970'), 
                      ('Western Sahara', ''), ('Yemen', '967'), ('Zambia', '260'), ('Zimbabwe', '263')]
        return tMatchList
        
        