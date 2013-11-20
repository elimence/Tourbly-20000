
from security import Root
from models import Tourist
from models import Guide
from google.appengine.ext import db
from google.appengine.api import urlfetch
import urllib
import json


def getCountryFromJson(jsonResponse):
    reponseResults = jsonResponse["results"]
    components_list = reponseResults[0]["address_components"]
    # return components_list[0]["types"][0][0]
    country = ""

    count = 0
    for component in components_list:
        component_type = components_list[count]["types"]
        
        if component_type[0] == "country":
            country = component["long_name"]

        count += 1

    return country

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

            request = urlfetch.Fetch("https://maps.googleapis.com/maps/api/geocode/json?address=" 
                + urllib.quote(search_args["destination"].encode("utf-8")) + "&sensor=true").content

            request_json = json.loads(request)
            destination_country = getCountryFromJson(request_json)

            suggested_guides = db.GqlQuery("select * from Guide where country = :1", destination_country)

            self.render("search.html", suggested_guides = suggested_guides, search_args = search_args)
    	else:
    		self.render("index.html", error_message = "Please provide all details to complete search")
