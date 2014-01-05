# @name    Booking.py
# @author  S. A.
# @date    Oct 13 13
# @purpose db model for Booking data


from security import Root
from google.appengine.ext import db
import Tourist
import Guide
import Destination

date = ""

class Booking(db.Model, Root.Handler):
    _tourist   = db.ReferenceProperty(Tourist.Tourist, collection_name = "tourist_booking_set")
    _guide     = db.ReferenceProperty(Guide.Guide, collection_name = "guide_booking_set")
    _place     = db.ReferenceProperty(Destination.Destination, collection_name = "place_booking_set")
    _tour_start   = db.DateTimeProperty()
    _tour_end = db.DateTimeProperty()
    _message = db.TextProperty()
    _description = db.StringProperty()
    _price = db.StringProperty()
    _payment_status = db.StringProperty(default = 'Completed')
    _booked_at = db.DateTimeProperty(auto_now_add = True)
    _booking_number = db.StringProperty()

