
import logging
from security import Root


class Logout(Root.Handler):
     def get(self):
     	logging.info("LOGOUT HANDLER CALLED")
        current_page = self.request.get("current_page")
        self.logout(["authenticator", "query"])
        self.redirect("/" + current_page)
