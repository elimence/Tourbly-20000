# @name    Guide.py
# @author  S. A.
# @date    Oct 11 13
# @purpose db model for Guide data


# from security import Root
from pyscripts import Utility
# import Review
from google.appengine.ext import db


date = ""


class Guide(db.Model,):
    _firstname   = db.StringProperty()
    _lastname    = db.StringProperty()
    _email       = db.EmailProperty()
    _phoneNumber = db.PhoneNumberProperty()
    _country     = db.StringProperty(required = True)
    _dateOfBirth = db.DateProperty()
    _gender      = db.StringProperty()
    _locations   = db.ListProperty(db.Key)
    _workDays    = db.ListProperty(db.Key)
    _picture     = db.StringProperty()
    _isAvailable = db.BooleanProperty(default = False)
    _times_booked = db.StringProperty()
    _lives_in    = db.StringProperty()
    _languages   = db.ListProperty(db.Key)
    # _rating      = db.ReferenceProperty(Review.Review, collection_name='reviews')
    _created_at  = db.DateTimeProperty(auto_now_add = True) 
