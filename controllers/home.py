
from security import Root
from models import Tourist
from datetime import datetime


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
        current_date = datetime.now()

        # arrival_date_obj = datetime.strptime(arrival_date, "%d %B, %Y")
        # departure_date_obj = datetime.strptime(departure_date, "%d-%B-%Y")
    	if destination and arrival_date and departure_date:
            self.redirect("/search?destination=" + destination + "&arrival_date=" + arrival_date
             + "&departure_date=" + departure_date)
    	self.render("index.html", error_message = "Please provide all details to complete search")
        
       