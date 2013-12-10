# @name    Review.py
# @author  S. A.
# @date    Oct 13 13
# @purpose db model for Review data


from security import Root
from google.appengine.ext import db
import Tourist
import Guide

date = ""

class Review(db.Model, Root.Handler):
    _reviewer = db.ReferenceProperty(Tourist.Tourist, collection_name = "reviewers_set")
    _reviewee = db.ReferenceProperty(Guide.Guide, collection_name = "reviews_set")
    _rating   = db.IntegerProperty()
    _comment  = db.TextProperty()
    _created_at = db.DateTimeProperty(auto_now_add = True)

