from security import Root
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

class Search(Root.Handler):
    def get(self):
    	destination = self.request.get("destination")
    	arrival_date = self.request.get("arrival_date")
    	departure_date = self.request.get("departure_date")

    	search_args = {"destination" : destination, "arrival_date" : arrival_date, "departure_date" : departure_date}

    	suggested_guides = None
    	if destination:
    		request = urlfetch.Fetch("https://maps.googleapis.com/maps/api/geocode/json?address=" 
                + urllib.quote(search_args["destination"].encode("utf-8")) + "&sensor=true").content

    		request_json = json.loads(request)
    		destination_country = getCountryFromJson(request_json)

    		suggested_guides = Guide.Guide.gql("where _country = :1", destination_country)

        self.render("search.html", suggested_guides = suggested_guides, search_args = search_args)
        
        	