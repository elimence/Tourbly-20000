# @Sam / @Chris: I created this file only to help me render the booking page
# Feel free to edit and add functionality as needed
from security import Root
from models import Guide    
from models import Tourist
from models import Review

class BookingHandler(Root.Handler):
  def get(self, guide_id):
    self.render("booking.html", isLoggedIn = self.check_session("query"))