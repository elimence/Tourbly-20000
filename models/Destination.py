from google.appengine.ext import ndb

class Destination(ndb.Model):
	name = ndb.StringProperty(required = True)
	latlng = ndb.StringProperty(required = True)
	description = ndb.TextProperty(required = True)
	region = ndb.StringProperty()
	city = ndb.StringProperty()
	direction = ndb.TextProperty()
	pictures = ndb.BlobProperty(repeated = True)

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
	def getAllDestination(cls):
		return cls.all()

	@staticmethod
	def checkDestinationExists(name, latlng):
		return Destination.filter("name=", name).get(), Destination.filter("latlng=", latlng).get()


	
