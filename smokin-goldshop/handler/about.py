from handler.base import BaseHandler

class AboutHandler(BaseHandler):
    LOCATION = "../views/about.html"
    def GetContext(self):
        return {}