
import logging
from security import Root
from models import Tourist
from datetime import datetime

class Bookings(Root.Handler):
  def get(self):
    if self.check_session("query"):
      tourist_id = int(self.get_cookie("query")[0])
      tourist = Tourist.Tourist.get_by_id(tourist_id)
      
      self.render("bookings.html", isLoggedIn = self.check_session("query"), tourist = tourist)
    else:
      self.redirect("/home")