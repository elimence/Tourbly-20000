from google.appengine.ext import db

class Destination(db.Model):
	name = db.StringProperty(required = True)
	latlng = db.StringProperty(required = True)
	description = db.TextProperty(required = True)
	region = db.StringProperty()
	city = db.StringProperty()
	direction = db.TextProperty()
	pictures = db.ArrayProperty()

	@classmethod
	def addDestination(cls, name, latlng, description):
		existing_destination, existing_destination2 = checkDestinationExists(name, latlng)

		if existing_destination or existing_destination2:
			return False, None
		else:
			destination = cls(name = name, latlng = latlng, description = description)
			destination.put()
			return True, destination

	@staticmethod
	def checkDestinationExists(name, latlng):
		return Destination.filter("name=", name).get(), Destination.filter("latlng=", latlng).get()


	
