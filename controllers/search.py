from security import Root
from models import Guide


class Search(Root.Handler):
    def get(self):
    	suggested_guides = Guide.Guide.all()
    	destination = self.request.get("destination")
    	arrival_date = self.request.get("arrival_date")
    	departure_date = self.request.get("departure_date")
    	
    	search_args = {"destination" : destination, "arrival_date" : arrival_date, "departure_date" : departure_date}
        self.render("search.html", suggested_guides = suggested_guides, search_args = search_args)