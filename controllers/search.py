from security import Root
from models import Guide
from models import Tourist
from google.appengine.ext import db
from google.appengine.api import urlfetch
import urllib
import json

all_languages = ["Afrikaans", "Albanian", "Arabic", "Armenian", "Basque", "Bengali", "Bulgarian",
 "Catalan", "Cambodian", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian",
 "Fiji", "Finnish", "French", "Georgian", "German", "Greek", "Gujarati", "Hebrew", "Hindi", "Hungarian",
 "Icelandic", "Indonesian", "Irish", "Italian", "Japanese", "Javanese", "Korean", "Latin", "Latvian",
 "Lithuanian", "Macedonian", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Nepali",
 "Norwegian", "Persian", "Polish", "Portuguese", "Punjabi", "Quechua", "Romanian", "Russian", "Samoan",
 "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tamil", "Tatar", "Telugu", "Thai",
 "Tibetan", "Tonga", "Turkish", "Ukrainian", "Urdu", "Uzbek", "Vietnamese", "Welsh", "Xhosa"]

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

    if gender == "Any" and language == "Any":
        suggested_guides = Guide.Guide.gql("where _country = :1 and _isAvailable = :2 limit 12",
         destination_country, True)
    elif language == "Any":
        suggested_guides = Guide.Guide.gql("where _country = :1 and _isAvailable = :2 and _gender = :3 limit 12",
         destination_country, True, gender)
    elif gender == "Any":
        suggested_guides = Guide.Guide.gql("where _country = :1 and _isAvailable = :2 and _languages = :3 limit 12",
         destination_country, True, language)
    elif gender != "Any" and gender != "" and language != "Any" and language != "":
        suggested_guides = Guide.Guide.gql("where _country = :1 and _isAvailable = :2 and _gender = :3 and _languages = :4 limit 12",
         destination_country, True, gender, language)
    else:
        suggested_guides = Guide.Guide.gql("where _country = :1 and _isAvailable = :2 limit 12",
         destination_country, True)

    return suggested_guides

def getGuidesWithLanguage(suggested_guides, language):
    actual_suggested_guides = []
    for suggested_guide in suggested_guides:
        if language in suggested_guide._languages:
            # suggested_guides.append(suggested_guide)
            actual_suggested_guides.append(suggested_guide)

    return actual_suggested_guides


class Search(Root.Handler, Root.Utility):
    def get(self):
        _id = self.get_user_id()
        if _id == -1000:
            return self.redirect('signin')

        tourist = Tourist.Tourist.get_by_id(_id)
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
            destination_country = self.getCountryFromJson(request_json)

        suggested_guides = getSuggestedGuidesQuery(destination, arrival_date, departure_date, gender,
         language, destination_country)

        if self.check_session("query"):
            tourist = Tourist.Tourist.get_by_id(self.get_user_id())
            self.render("search.html", suggested_guides = suggested_guides, isLoggedIn = self.check_session("query"),
             tourist = tourist, search_args = search_args, all_languages = all_languages)
        else:
            self.render("search.html", suggested_guides = suggested_guides, isLoggedIn = self.check_session("query"),
             tourist = tourist, search_args = search_args, all_languages = all_languages)

    def post(self):
        destination = self.request.get("destination")
        arrival_date = self.request.get("arrival")
        departure_date = self.request.get("departure")
        gender = self.request.get("gender")
        language = self.request.get("language")

        self.redirect("/search?destination=" + destination + "&arrival_date=" + arrival_date
         + "&departure_date=" + departure_date + "&gender=" + gender + "&language=" + language)
        

