
from security import Root
from models import Tourist
from models import Guide
from google.appengine.ext import db


class Home(Root.Handler):
    def get(self):
        if self.check_session("query"):
            tourist = Tourist.Tourist.get_by_id(self.get_user_id())
            self.render("index.html", isLoggedIn = self.check_session("query"), tourist = tourist)
        else:
            self.render("index.html", isLoggedIn = self.check_session("query"))

    def post(self):
    	destination = self.request.get("destination")
    	arrival_date = self.request.get("arrival")
    	departure_date = self.request.get("departure")

    	if destination and arrival_date and departure_date:
    		search_args = {"destination" : destination, "arrival_date" : arrival_date, "departure_date" : departure_date}
    		suggested_guides = db.GqlQuery("select * from Guide")
    		self.render("search.html", suggested_guides = suggested_guides, search_args = search_args)
    	else:
    		self.render("index.html", error_message = "Please provide all details to complete search")
