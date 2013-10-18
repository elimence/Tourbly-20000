# from security import Root
from google.appengine.ext import db
# import Helper

class Tourist(db.Model):
	firstName = db.StringProperty()
	lastName = db.StringProperty()
	email = db.EmailProperty(required = True)
	password = db.StringProperty(required = True)
	country = db.StringProperty()
	state = db.StringProperty()
	languages = db.ListProperty(db.Key)
	salt = db.StringProperty(required = True)
	picture = db.BlobProperty()
	activated = db.BooleanProperty(default = False)
	token = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add = True)

	# @classmethod
	@staticmethod
	def addTourist(email, hashed_password, salt, token):
		tourist = Tourist(email = email, password = str(hashed_password), salt = salt, token = token)
		tourist.put()
		return tourist

	@classmethod 
	def verifyTourist(cls, email, password):
		status, tourist = Helper.verify_user(email, password, "tourist")

		if status:
			return tourist

	@classmethod 
	def getTourist(cls, email):
		return cls.filter("email=", email).get()

	@classmethod
	def getAllTourists(cls):
		return cls.all()
