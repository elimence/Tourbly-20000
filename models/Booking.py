# @name    Booking.py
# @author  S. A.
# @date    Oct 13 13
# @purpose db model for Review data


from security import Root
from google.appengine.ext import db
import Tourist
import Guide

date = ""

class Booking(db.Model, Root.Handler):
    _tourist   = db.ReferenceProperty(Tourist.Tourist, collection_name = "tourist_booking_set")
    _guide     = db.ReferenceProperty(Guide.Guide, collection_name = "guide_booking_set")
    _tour_start   = db.DateTimeProperty()
    _tour_end = db.DateTimeProperty()
    _message = db.TextProperty()
    _booked_at = db.DateTimeProperty(auto_now_add = True)

