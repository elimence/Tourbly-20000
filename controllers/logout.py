
import logging
from security import Root


class Logout(Root.Handler):
     def get(self):
        referer = self.request.referer
        if referer:
            referer = referer[referer.find("/", 8) : ]
        self.write(referer)
        self.logout(["authenticator", "query"])
        self.redirect(referer)
