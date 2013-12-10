from security import Root
from models import Tourist
from models import Destination


class Places(Root.Handler):
    def get(self):
    	tourist = Tourist.Tourist.get_by_id(self.get_user_id())
        places = Destination.Destination.getAllDestination()
        self.render("places.html", places = places, isLoggedIn = self.check_session("query"), tourist=tourist)


# @nanaewusi - to whom it may concern
# I only added this class to help me render a place profile page on the UI side
# A proper implementation is required for in order to dynamically show a place profile
# Please proceed to implement this class

class ShowPlace(Root.Handler):    
  def get(self):
    self.render("place.html")