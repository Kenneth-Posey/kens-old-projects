
import re, logging
from models.price import Price

class PriceContainer():
    
    @staticmethod
    def GetBasePriceDictionary():
        tPriceDict = {            
                        '0001m':'0',            
                        '0002m':'0',            
                        '0003m':'0',            
                        '0004m':'0',            
                        '0005m':'0',            
                        '0006m':'0',            
                        '0007m':'0',            
                        '0008m':'0',            
                        '0009m':'0',            
                        '0010m':'0',            
                        '0011m':'0',            
                        '0012m':'0',            
                        '0013m':'0',            
                        '0014m':'0',            
                        '0015m':'0',
                        '0020m':'0',
                        '0025m':'0',
                        '0030m':'0',
                        '0035m':'0',
                        '0040m':'0',
                        '0050m':'0',
                        '0060m':'0',
                        '0070m':'0',
                        '0080m':'0',
                        '0090m':'0',
                        '0100m':'0',
                        '0150m':'0',
                        '0200m':'0',
                        '0300m':'0',
                        '0400m':'0',
                        '0500m':'0',
                        '0600m':'0',
                        '0700m':'0',
                        '0800m':'0',
                        '0900m':'0',
                        '1000m':'0'
                    }                     
        return tPriceDict
    
    @staticmethod    
    def GetBasePriceDictionaryWithoutZeros():
        tBasePrices = PriceContainer.GetBasePriceDictionary()
        
        tPriceList = []
        tSortedPriceKeys = sorted(tBasePrices.keys())
        
        tCleanPriceDictionary = {}
        for tCurrentKey in tSortedPriceKeys:
            if(tCurrentKey[:3] == '000'):
                tKey = tCurrentKey[3:]
            elif(tCurrentKey[:2] == '00'):
                tKey = tCurrentKey[2:]
            elif(tCurrentKey[0] == '0'):
                tKey = tCurrentKey[1:]
            else:
                tKey = tCurrentKey
                
            tCleanPriceDictionary[tKey] = str(tBasePrices[tCurrentKey])
            #tCleanPriceDictionary[tKey.upper()] = str(tBasePrices[tCurrentKey])
                
        return tCleanPriceDictionary        
        
    """
    Returns Current Goldshop Prices
    """
    @staticmethod
    #Can not end with 0
    def GetCurrentPriceDic():
        tCurrentPrice = Price()
        tPriceQuery = Price().all()
        tPriceQuery.order("-priceDateCreated")
        tPriceQuery.filter("priceType", 'regular')
        tCurrentPrice = tPriceQuery.fetch(limit=1)[0]
            
        tPriceDictionary = PriceContainer.GetBasePriceDictionary()
        
        tSortedProperties = sorted(tCurrentPrice.properties().keys())
        for tCurrentProperty in tSortedProperties:
            try:
                tMatches = re.match(r'price(?P<number>[0-9]{4}m)', str(tCurrentProperty))
                tMatchedKey = str(tMatches.group('number'))
                
                tPriceDictionary[tMatchedKey] = tCurrentPrice.__getattribute__(tCurrentProperty)
            except:
                logging.debug('Could not find a key in: ' + str(tCurrentProperty))
        
        tPriceList = []
        tSortedPriceKeys = sorted(tPriceDictionary.keys())
        
        tCleanPriceDictionary = {}
        for tCurrentKey in tSortedPriceKeys:
            if(tCurrentKey[:3] == '000'):
                tKey = tCurrentKey[3:]
            elif(tCurrentKey[:2] == '00'):
                tKey = tCurrentKey[2:]
            elif(tCurrentKey[:1] == '0'):
                tKey = tCurrentKey[1:]
            else:
                tKey = tCurrentKey
                
            tCleanPriceDictionary[tKey] = str(tPriceDictionary[tCurrentKey])
            tCleanPriceDictionary[tKey.upper()] = str(tPriceDictionary[tCurrentKey])
                
        return tCleanPriceDictionary

    """
    Returns Current 07 Goldshop Prices
    """
    @staticmethod
    #Can not end with 0
    def GetCurrentPriceDic07():
        tCurrentPrice = Price()
        tPriceQuery = Price().all()
        tPriceQuery.order("-priceDateCreated")
        tPriceQuery.filter("priceType", '07')
        tCurrentPrice = tPriceQuery.fetch(limit=1)[0]
            
        tPriceDictionary = PriceContainer.GetBasePriceDictionary()  
        
        tSortedProperties = sorted(tCurrentPrice.properties().keys())
        for tCurrentProperty in tSortedProperties:
            try:
                tMatches = re.match(r'price(?P<number>[0-9]{4}m)', str(tCurrentProperty))
                tMatchedKey = str(tMatches.group('number'))
                
                tPriceDictionary[tMatchedKey] = tCurrentPrice.__getattribute__(tCurrentProperty)
            except:
                logging.debug('Could not find a key in: ' + str(tCurrentProperty))
        
        tPriceList = []
        tSortedPriceKeys = sorted(tPriceDictionary.keys())
        
        tCleanPriceDictionary = {}
        for tCurrentKey in tSortedPriceKeys:
            if(tCurrentKey[:3] == '000'):
                tKey = tCurrentKey[3:]
            elif(tCurrentKey[:2] == '00'):
                tKey = tCurrentKey[2:]
            elif(tCurrentKey[0] == '0'):
                tKey = tCurrentKey[1:]
            else:
                tKey = tCurrentKey
                
            tCleanPriceDictionary[tKey] = str(tPriceDictionary[tCurrentKey])
            tCleanPriceDictionary[tKey.upper()] = str(tPriceDictionary[tCurrentKey])
                
        return tCleanPriceDictionary

class CountryContainer():
    """
    Returns Country Abbreviations
    """
    @staticmethod
    def GetCurrentCountryCodes():
        tCountries = {'BD': 'Bangladesh', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria', 'BA': 'Bosnia and Herzegovina', 
                      'BB': 'Barbados', 'WF': 'Wallis and Futuna Islands', 'BM': 'Bermuda', 'BN': 'Brunei Darussalam', 'BO': 'Bolivia', 
                      'BH': 'Bahrain', 'BI': 'Burundi', 'BJ': 'Benin', 'BT': 'Bhutan', 'JM': 'Jamaica', 'BV': 'Bouvet Island', 
                      'BW': 'Botswana', 'WS': 'Samoa', 'BR': 'Brazil', 'BS': 'Bahamas', 'JE': 'Jersey', 'BY': 'Belarus', 'BZ': 'Belize', 
                      'RU': 'Russian Federation', 'RW': 'Rwanda', 'RS': 'Serbia', 'RE': 'Reunion', 'TM': 'Turkmenistan', 'TJ': 'Tajikistan', 
                      'RO': 'Romania', 'TK': 'Tokelau', 'GW': 'Guinea-Bissau', 'GU': 'Guam', 'GT': 'Guatemala', 'GS': 'S. Georgia and S. Sandwich Isls.', 
                      'GR': 'Greece', 'GQ': 'Equatorial Guinea', 'GP': 'Guadeloupe', 'JP': 'Japan', 'GY': 'Guyana', 'GG': 'Guernsey', 'GF': 'French Guiana', 
                      'GE': 'Georgia', 'GD': 'Grenada', 'GB': 'Great Britain (UK)', 'GA': 'Gabon', 'SV': 'El Salvador', 'GN': 'Guinea', 'GM': 'Gambia', 
                      'GL': 'Greenland', 'GI': 'Gibraltar', 'GH': 'Ghana', 'OM': 'Oman', 'TN': 'Tunisia', 'JO': 'Jordan', 'HR': 'Croatia (Hrvatska)', 
                      'HT': 'Haiti', 'HU': 'Hungary', 'HK': 'Hong Kong', 'HN': 'Honduras', 'SU': 'USSR (former)', 'HM': 'Heard and McDonald Islands', 
                      'VE': 'Venezuela', 'PR': 'Puerto Rico', 'PS': 'Palestinian Territory, Occupied', 'PW': 'Palau', 'PT': 'Portugal', 'SJ': 'Svalbard & Jan Mayen Islands', 
                      'PY': 'Paraguay', 'IQ': 'Iraq', 'PA': 'Panama', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea', 'PE': 'Peru', 'PK': 'Pakistan', 'PH': 'Philippines', 
                      'PN': 'Pitcairn', 'PL': 'Poland', 'PM': 'St. Pierre and Miquelon', 'ZM': 'Zambia', 'EH': 'Western Sahara', 'EE': 'Estonia', 'EG': 'Egypt', 
                      'ZA': 'South Africa', 'EC': 'Ecuador', 'IT': 'Italy', 'UK': 'United Kingdom', 'VN': 'Viet Nam', 'SB': 'Solomon Islands', 'EU': 'European Union', 
                      'ET': 'Ethiopia', 'SO': 'Somalia', 'SA': 'Saudi Arabia', 'ES': 'Spain', 'ER': 'Eritrea', 'ME': 'Montenegro', 'MD': 'Moldova', 'MG': 'Madagascar', 
                      'MA': 'Morocco', 'MC': 'Monaco', 'UZ': 'Uzbekistan', 'MM': 'Myanmar', 'ML': 'Mali', 'MO': 'Macau', 'MN': 'Mongolia', 'MH': 'Marshall Islands', 
                      'MK': 'F.Y.R.O.M. (Macedonia)', 'MU': 'Mauritius', 'MT': 'Malta', 'MW': 'Malawi', 'MV': 'Maldives', 'MQ': 'Martinique', 'MP': 'Northern Mariana Islands', 
                      'MS': 'Montserrat', 'MR': 'Mauritania', 'IM': 'Isle of Man', 'UG': 'Uganda', 'TZ': 'Tanzania', 'MY': 'Malaysia', 'MX': 'Mexico', 'IL': 'Israel', 
                      'FR': 'France', 'IO': 'British Indian Ocean Territory', 'FX': 'France, Metropolitan', 'SH': 'St. Helena', 'FI': 'Finland', 'FJ': 'Fiji', 
                      'FK': 'Falkland Islands (Malvinas)', 'FM': 'Micronesia', 'FO': 'Faroe Islands', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 
                      'NA': 'Namibia', 'VU': 'Vanuatu', 'NC': 'New Caledonia', 'NE': 'Niger', 'NF': 'Norfolk Island', 'NG': 'Nigeria', 'NZ': 'New Zealand (Aotearoa)', 
                      'NP': 'Nepal', 'NR': 'Nauru', 'NT': 'Neutral Zone', 'NU': 'Niue', 'CK': 'Cook Islands', 'CI': "Cote D'Ivoire (Ivory Coast)", 'CH': 'Switzerland', 
                      'CO': 'Colombia', 'CN': 'China', 'CM': 'Cameroon', 'CL': 'Chile', 'CC': 'Cocos (Keeling) Islands', 'CA': 'Canada', 'CG': 'Congo', 
                      'CF': 'Central African Republic', 'CD': 'Congo, Democratic Republic', 'CZ': 'Czech Republic', 'CY': 'Cyprus', 'CX': 'Christmas Island', 
                      'CS': 'Czechoslovakia (former)', 'CR': 'Costa Rica', 'CV': 'Cape Verde', 'CU': 'Cuba', 'SZ': 'Swaziland', 'SY': 'Syria', 'KG': 'Kyrgyzstan', 
                      'KE': 'Kenya', 'SR': 'Suriname', 'KI': 'Kiribati', 'KH': 'Cambodia', 'KN': 'Saint Kitts and Nevis', 'KM': 'Comoros', 'ST': 'Sao Tome and Principe', 
                      'SK': 'Slovak Republic', 'KR': 'Korea (South)', 'SI': 'Slovenia', 'KP': 'Korea (North)', 'KW': 'Kuwait', 'SN': 'Senegal', 'SM': 'San Marino', 
                      'SL': 'Sierra Leone', 'SC': 'Seychelles', 'KZ': 'Kazakhstan', 'KY': 'Cayman Islands', 'SG': 'Singapore', 'SE': 'Sweden', 'SD': 'Sudan', 
                      'DO': 'Dominican Republic', 'DM': 'Dominica', 'DJ': 'Djibouti', 'DK': 'Denmark', 'VG': 'British Virgin Islands ', 'DE': 'Germany', 'YE': 'Yemen', 
                      'DZ': 'Algeria', 'US': 'United States', 'UY': 'Uruguay', 'YU': 'Serbia and Montenegro (former)', 'YT': 'Mayotte', 'UM': 'US Minor Outlying Islands', 
                      'LB': 'Lebanon', 'LC': 'Saint Lucia', 'LA': 'Laos', 'TV': 'Tuvalu', 'TW': 'Taiwan', 'TT': 'Trinidad and Tobago', 'TR': 'Turkey', 'LK': 'Sri Lanka', 
                      'TP': 'East Timor', 'LI': 'Liechtenstein', 'LV': 'Latvia', 'TO': 'Tonga', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LR': 'Liberia', 'LS': 'Lesotho', 
                      'TH': 'Thailand', 'TF': 'French Southern Territories', 'TG': 'Togo', 'TD': 'Chad', 'TC': 'Turks and Caicos Islands', 'LY': 'Libya', 
                      'VA': 'Vatican City State (Holy See)', 'AC': 'Ascension Island', 'VC': 'Saint Vincent & the Grenadines', 'AE': 'United Arab Emirates', 
                      'AD': 'Andorra', 'AG': 'Antigua and Barbuda', 'AF': 'Afghanistan', 'AI': 'Anguilla', 'VI': 'Virgin Islands (U.S.)', 'IS': 'Iceland', 
                      'IR': 'Iran', 'AM': 'Armenia', 'AL': 'Albania ', 'AO': 'Angola', 'AN': 'Netherlands Antilles', 'AQ': 'Antarctica', 'AS': 'American Samoa', 
                      'AR': 'Argentina', 'AU': 'Australia', 'AT': 'Austria', 'AW': 'Aruba', 'IN': 'India', 'AX': 'Aland Islands', 'AZ': 'Azerbaijan', 
                      'IE': 'Ireland', 'ID': 'Indonesia', 'UA': 'Ukraine', 'QA': 'Qatar', 'MZ': 'Mozambique'}
        return tCountries
    
class TierContainer():
    @staticmethod
    def GetVipTierInfo():
        
        tSubscriptionTierGrades = {
                                "Tier1": ("Tier0", (0, 30)),
                                "Tier2": ("Tier1", (31, 60)),
                                "Tier3": ("Tier2", (61, 120)),
                                "Tier4": ("Tier3", (121, 5000))
                                }
        
        return tSubscriptionTierGrades