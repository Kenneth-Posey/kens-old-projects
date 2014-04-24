
from models.paorder import PaOrder
from base import BaseHandler

class PASummary(BaseHandler):
    LOCATION = '../views/pa.html'
    def GetContext(self):
        tContext = {}
        tPaList = []
        
        tOffset = 0
        
        tStringOffset = self.request.get('offset')
        if (len(tStringOffset) > 0):
            tOffset = int(tStringOffset)
        else:
            tOffset = 0
            
        if (tOffset == 0):
            tPrev = tOffset
        else: 
            tPrev = tOffset - 20
        tOffset = tOffset + 20
        tNext = tOffset
        
        tOffset = str(tOffset)
        tNext = str(tNext)
        tPrev = str(tPrev)
        
        tContext['next'] = str(tNext)
        tContext['prev'] = str(tPrev)
        
        tPa = PaOrder().all()
        tPa.order('-paDate')
        tPaList = tPa.fetch(limit=20, offset = int(tOffset))
        tContext['palist'] = tPaList
        
        return tContext