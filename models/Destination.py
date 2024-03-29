
from google.appengine.ext import db
from security import Root

class Destination(db.Model, Root.Handler):
	name = db.StringProperty(required = True)
	latlng = db.StringProperty(required = True)
	description = db.TextProperty(required = True)
	tagline = db.StringProperty()
	country = db.StringProperty()
	region = db.StringProperty()
	city = db.StringProperty()
	direction = db.TextProperty()
	times_visited = db.IntegerProperty()
	pictures = db.StringListProperty()
	pictures_blobs = db.ListProperty(db.Blob)
	tags = db.StringListProperty()
	keywords = db.StringListProperty()

	@classmethod
	def addDestination(cls, name, latlng, description):
		existing_destination, existing_destination2 = checkDestinationExists(name, latlng)

		if existing_destination or existing_destination2:
			return False, None
		else:
			destination = cls(name = name, latlng = latlng, description = description)
			destination.put()
			return True, destination

	@classmethod
	def getDestination(cls, name):
		return cls.filter("name=", name).get()

	@classmethod
	def getAllDestinations(cls):
		return cls.all()

	@staticmethod
	def checkDestinationExists(name, latlng):
		return Destination.filter("name=", name).get(), Destination.filter("latlng=", latlng).get()



