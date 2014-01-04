
from security import Root
from models import Tourist
from datetime import datetime
from models import Destination
import logging


class Home(Root.Handler):
    def get(self):
        places = Destination.Destination.gql("limit 6")
        all_places = Destination.Destination.all().run()   #@nanaewusi - I added this to get an initial dump of the places for the dropdown
        if self.check_session("query"):
            tourist = Tourist.Tourist.get_by_id(self.get_user_id())
            self.render("index.html", isLoggedIn = self.check_session("query"), tourist = tourist, 
                places = places, all_places = all_places)
        else:
            self.render("index.html", isLoggedIn = self.check_session("query"), places = places, 
                        all_places = all_places)

    def post(self):
        all_places = Destination.Destination.all().run()   #@nanaewusi - I added this to get an initial dump of the places for the dropdown
        places = Destination.Destination.gql("limit 6")
    	destination = self.request.get("destination")
    	arrival_date = self.request.get("arrival")
    	departure_date = self.request.get("departure")
        current_date = datetime.now()

        logging.info(arrival_date)

    	if destination and arrival_date and departure_date:
            self.redirect("/search?destination=" + destination + "&arrival_date=" + arrival_date
             + "&departure_date=" + departure_date)
    	self.render("index.html", error_message = "Please provide all details to complete search", 
            places = places, all_places = all_places)
        
class About(Root.Handler):
    def get(self):
        featured_places = Destination.Destination.gql("limit 3")
        if self.check_session("query"):
            tourist = Tourist.Tourist.get_by_id(self.get_user_id())
            self.render("about.html", isLoggedIn = self.check_session("query"), tourist = tourist, 
                featured_places = featured_places)
        else:
            self.render("about.html", isLoggedIn = self.check_session("query"), featured_places = featured_places)

class Contact(Root.Handler):
    def get(self):
        if self.check_session("query"):
            tourist = Tourist.Tourist.get_by_id(self.get_user_id())
            self.render("contact.html", isLoggedIn = self.check_session("query"), tourist = tourist)
        else:
            self.render("contact.html", isLoggedIn = self.check_session("query"))

