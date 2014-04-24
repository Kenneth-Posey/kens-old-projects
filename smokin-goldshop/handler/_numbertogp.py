
import re, logging

class NumberToGp():
    @staticmethod
    def ConvertBetToInt(pWager):
        tNegative = False
        if (pWager == 'Bulk'):
            pWager = "100m"
        if(pWager[0] == '-'):
            pWager = pWager[1:]
            tNegative = True
        tBet = pWager[:-1] # removes unit
        tBet = tBet.replace(",", "")
        tBet = float(tBet)
        
        tMuliplier = NumberToGp.GetMultiplier(pWager)
        tWager = tBet * tMuliplier
        
        if tNegative:
            tWager = tWager * -1 
        
        return int(tWager)
    
    @staticmethod    
    def GetMultiplier(pWager):
        tUnit = pWager[-1:]
        
        if(tUnit == "b" or tUnit == "B"):
            tMultiplier = 1000000000
        elif(tUnit == "m" or tUnit == "M"):
            tMultiplier = 1000000
        elif(tUnit == "k" or tUnit == "K"):
            tMultiplier = 1000
        else:
            tMultiplier = 1
            
        return tMultiplier
    
    @staticmethod
    def ConvertIntToBet(pBet):
        tBet = str(pBet)
        tNegative = False
        #logging.debug("Gold Amount: " + tBet)
        
        if tBet[0] == '-':
            tBet = tBet[1:]
            tNegative = True
            
        tLength = len(tBet)
        if (tLength > 3 and tLength <= 6):
            tLastHalf = tBet[-3:]
            #tRemainder = re.sub("[0]", "", str(tLastHalf))
            while tLastHalf[-1:] == '0':
                tLastHalf = tLastHalf[:-1]
            tRemainder = tLastHalf
            tFirstHalf = tBet[:-3]
            if (len(tRemainder) == 0):
                tBetWord = tFirstHalf + "k"
            else:
                tBetWord = tFirstHalf + "." + tRemainder + "k"
                
        elif(tLength > 6 and tLength <= 9):
            tLastHalf = tBet[-6:]
            #tRemainder = re.sub("[0]", "", str(tLastHalf))
            while tLastHalf[-1:] == '0':
                tLastHalf = tLastHalf[:-1]
            tRemainder = tLastHalf
            tFirstHalf = tBet[:-6]
            if (len(tRemainder) == 0):
                tBetWord = tFirstHalf + "m"
            else:
                tBetWord = tFirstHalf + "." + tRemainder + "m"
        elif(tLength > 9):
            tLastHalf = tBet[-9:]
            #tRemainder = re.sub("[0]", "", str(tLastHalf))
            while tLastHalf[-1:] == '0':
                tLastHalf = tLastHalf[:-1]
            tRemainder = tLastHalf
            tFirstHalf = tBet[:-9]
            if (len(tRemainder) == 0):
                tBetWord = tFirstHalf + "b"
            else:
                tBetWord = tFirstHalf + "." + tRemainder + "b"
        else:
            tBetWord = tBet
        
        if tNegative:
            tBetWord = '-' + tBetWord
        
        return tBetWord    