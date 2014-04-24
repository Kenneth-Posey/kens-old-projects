import datetime

class TimeHelperMethods():
    @staticmethod
    def HoursAgo(pHours):
        return datetime.datetime.now() - datetime.timedelta(hours = pHours)
        
    @staticmethod
    def DaysAgo(pDays):        
        return datetime.datetime.now() - datetime.timedelta(days = pDays)