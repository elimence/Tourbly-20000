from security import Root
from models import Tourist
from models import Destination


class Places(Root.Handler):
    def get(self):
    	tourist = Tourist.Tourist.get_by_id(self.get_user_id())
        places = Destination.Destination.getAllDestination()
        self.render("places.html", places = places, isLoggedIn = self.check_session("query"), tourist=tourist)
