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

def getSuggestedGuidesQuery(destination, arrival_date, departure_date, gender, language, 
    destination_country):
    suggested_guides = None

    if gender == "Any" and language == "None":
        suggested_guides = Guide.Guide.gql("where _country = :1 and _isAvailable = :2 limit 12",
         destination_country, True)
    elif language == "None":
        suggested_guides = Guide.Guide.gql("where _country = :1 and _isAvailable = :2 and _gender = :3 limit 12",
         destination_country, True, gender)
    elif gender == "Any":
        suggested_guides = Guide.Guide.gql("where _country = :1 and _isAvailable = :2 and limit 12",
         destination_country, True)
    else:
        suggested_guides = Guide.Guide.gql("where _country = :1 and _isAvailable = :2 and _gender = :3 limit 12",
         destination_country, True, gender)
        
    return suggested_guides

# def getQueryWithLanguage(suggested_guides, language):


class Search(Root.Handler):
    def get(self):
    	destination = self.request.get("destination")
    	arrival_date = self.request.get("arrival_date")
    	departure_date = self.request.get("departure_date")
        gender = self.request.get("gender")
        language = self.request.get("language")

    	search_args = {"destination" : destination, "arrival_date" : arrival_date, "departure_date" : departure_date,
        "gender" : gender, "language" : language}

        destination_country = ""
    	if destination:
            request = urlfetch.Fetch("https://maps.googleapis.com/maps/api/geocode/json?address=" 
                + urllib.quote(search_args["destination"].encode("utf-8")) + "&sensor=true").content

            request_json = json.loads(request)
            destination_country = getCountryFromJson(request_json)

        suggested_guides = getSuggestedGuidesQuery(destination, arrival_date, departure_date, gender,
         language, destination_country)

        self.render("search.html", suggested_guides = suggested_guides, search_args = search_args)
        
    def post(self):
        destination = self.request.get("destination")
        arrival_date = self.request.get("arrival")
        departure_date = self.request.get("departure")
        gender = self.request.get("gender")
        language = self.request.get("language")

        self.redirect("/search?destination=" + destination + "&arrival_date=" + arrival_date
         + "&departure_date=" + departure_date + "&gender=" + gender + "&language=" + language)
        self.render("index.html", error_message = "Please provide all details to complete search")
        	