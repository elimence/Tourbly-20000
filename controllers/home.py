
from security import Root
from models import Tourist


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
    		# self.render("search.html")
    		self.write(destination + " " + arrival_date + " " + departure_date)
    		suggested_guides = Guide.qql()
    		self.render("search.html", suggested_guides = suggested_guides)
    	else:
    		self.render("index.html", error_message = "Please provide all details to complete search")
