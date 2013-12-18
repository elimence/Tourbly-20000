from security import Root
from models import Tourist
from models import Destination
from models import Guide

class PlaceHandler(Root.Handler):
	def get(self, place_id):
		place = Destination.Destination.get_by_id(int(place_id))

		available_guides = None
		if place:
			available_guides = Guide.Guide.gql("where _isAvailable = :1", True)

		if self.check_session("query"):
			tourist = Tourist.Tourist.get_by_id(self.get_user_id())
			self.render("place.html", place = place, isLoggedIn = self.check_session("query"), 
				tourist = tourist, available_guides = available_guides)
		else:
			self.render("place.html", place = place, isLoggedIn = self.check_session("query"), 
				available_guides = available_guides)
		