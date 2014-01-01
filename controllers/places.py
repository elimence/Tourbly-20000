from security import Root
from models import Tourist
from models import Destination
from google.appengine.ext import db


class Places(Root.Handler):
    def get(self):
    	tourist = Tourist.Tourist.get_by_id(self.get_user_id())
        places = Destination.Destination.getAllDestinations()
        keyword = self.request.get("keyword")

        if keyword:
        	places = Destination.Destination.gql("where tags = :1" ,keyword.lower())
        self.render("places.html", places = places, isLoggedIn = self.check_session("query"), tourist=tourist,
         keyword = keyword)

    def post(self):
    	keyword = self.request.get("keyword")
    	self.redirect("/places?keyword=" + keyword.lower())


# @nanaewusi - to whom it may concern
# I only added this class to help me render a place profile page on the UI side
# A proper implementation is required for in order to dynamically show a place profile
# Please proceed to implement this class

class ShowPlace(Root.Handler):    
  def get(self):
    self.render("place.html")