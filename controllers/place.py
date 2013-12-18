from security import Root
from models import Tourist
from models import Destination

class PlaceHandler(Root.Handler):
	def get(self, place_id):
		place = Destination.Destination.get_by_id(int(place_id))

		if self.check_session("query"):
			tourist = Tourist.Tourist.get_by_id(self.get_user_id())
			self.render("place.html", place = place, isLoggedIn = self.check_session("query"), tourist = tourist)
		else:
			self.render("place.html", place = place, isLoggedIn = self.check_session("query"))
		