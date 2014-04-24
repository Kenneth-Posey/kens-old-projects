
import datetime

class StringMethods():
    @staticmethod
    def StringToDatetime(pString):
        tTimestampDecoded = urllib.unquote(pString)
        tTimestampSplit = str(tTimestampDecoded).split(' ')
        tTimestampDate = tTimestampSplit[0]
        tTimestampTime = tTimestampSplit[1]
        tTimestampDateSplit = tTimestampDate.split('-')
        tTimestampTimeSplit = tTimestampTime.split(':')
        
        tOrderTime = datetime.datetime(int(tTimestampDateSplit[0]), int(tTimestampDateSplit[1]), 
                                       int(tTimestampDateSplit[2]), int(tTimestampTimeSplit[0]),
                                       int(tTimestampTimeSplit[1]), int(tTimestampTimeSplit[2]))
        return tOrderTime
    
    @staticmethod
    def DatetimeToString(pDatetime):
        tDate = str(pDatetime.year) + "-" + str(pDatetime.month) + "-" + str(pDatetime.day)
        tTime = str(pDatetime.hour) + ":" + str(pDatetime.minute) + ":" + str(pDatetime.second)
        return tDate + " " + tTime