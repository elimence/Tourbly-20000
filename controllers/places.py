from security import Root
from models import Tourist
from models import Destination
from google.appengine.ext import db
import json


class Places(Root.Handler):
    def get(self):
    	tourist = Tourist.Tourist.get_by_id(self.get_user_id())
        # places = Destination.Destination.getAllDestinations()
        places_query = db.GqlQuery("select * from Destination")
        keyword = self.request.get("keyword")
        cursor = urlsafe=self.request.get("cursor")
        # query = Destination.Destination.query()

        if keyword:
        	# places = Destination.Destination.gql("where keywords = :1" ,keyword.lower())
            places_query = db.GqlQuery("select * from Destination where keywords = :1", keyword.lower())

        # items, next_curs, more = places.fetch(2, start_cursor = cursor)
        # if more:
        #     next_c = next_curs.urlsafe()
        # else:
        #     next_c = None
        # items = db.GqlQuery("select * from Destination limit 1")
        if cursor:
            # self.write(str(cursor))
            places_query.with_cursor(cursor)
        places = places_query.fetch(9)
        cursor = places_query.cursor()
        self.render("places.html", places = places, isLoggedIn = self.check_session("query"), tourist=tourist,
         keyword = keyword, cursor = cursor, places_query = places_query)

    def post(self):
    	keyword = self.request.get("keyword")
    	self.redirect("/places?keyword=" + keyword.lower())


# @nanaewusi - to whom it may concern
# I only added this class to help me render a place profile page on the UI side
# A proper implementation is required for in order to dynamically show a place profile
# Please proceed to implement this class

class ShowPlace(Root.Handler):    
  def get(self):
    self.render("place.html")

def getPlacesJson(places):
    places_json = {}
    places_json["status"] = "ok"
    places_json["message"] = "successful"

    places_array = []
    for place in places:
        place_object = {}
        place_object["name"] = place.name
        place_object["id"] = place.key().id()

        places_array.append(place_object)

    places_json["places"] = places_array

    return json.dumps(places_json)

class GetAllPlaces(Root.Handler):
    def get(self):
        places = Destination.Destination.all()
        places_json = getPlacesJson(places)

        self.write(places_json)
        
        