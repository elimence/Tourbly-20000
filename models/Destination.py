from google.appengine.ext import db

class Destination(db.Model):
	name = db.StringProperty(required = True)
	latlng = db.StringProperty(required = True)
	description = db.TextProperty(required = True)
	region = db.StringProperty()
	city = db.StringProperty()
	direction = db.TextProperty()
	pictures = db.ArrayProperty()

	
