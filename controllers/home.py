
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
            # guide = Guide.Guide(_country = "Ghana", _picture = "https://fbcdn-profile-a.akamaihd.net/static-ak/rsrc.php/v2/yo/r/UlIqmHJn-SK.gif",
            #     _firstname = "David", _lastname = "Thomson", _email = "david@gmail.com")
            # guide.put()
            # self.render("search.html", suggested_guides = suggested_guides, search_args = search_args)
            self.redirect("/search?destination=" + destination + "&arrival_date=" + arrival_date + "&departure_date=" + departure_date)
    	else:
    		self.render("index.html", error_message = "Please provide all details to complete search")
