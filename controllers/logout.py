
import logging
from security import Root


class Logout(Root.Handler):
     def get(self):
        current_page = self.request.get("current_page")
        self.logout(["authenticator", "query"])
        self.redirect("/" + current_page)
