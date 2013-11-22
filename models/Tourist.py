# from security import Root
from google.appengine.ext import db

class Tourist(db.Model):
	first_name	= db.StringProperty(default = "")
	last_name 	= db.StringProperty(default = "")
	email 		= db.EmailProperty(required = True)
	password 	= db.StringProperty()
	country 	= db.StringProperty(default = "")
	state 		= db.StringProperty(default = "")
	languages 	= db.ListProperty(db.Key)
	salt 		= db.StringProperty()
	picture 	= db.StringProperty()
	activated 	= db.BooleanProperty(default = False)
	token 		= db.StringProperty()
	created 	= db.DateTimeProperty(auto_now_add = True)
	gender 		= db.StringProperty() 							# NB: - NEW ADDITION


	# @classmethod
	@staticmethod
	def addTourist(email, hashed_password, salt, token, picture):
		tourist = Tourist(email = email, password = str(hashed_password), salt = salt, token = token, picture = picture)
		tourist.put()
		return tourist


	@staticmethod
	def create_from_oauth(email, first_name, last_name, gender, picture, activated):
		tourist = Tourist(email=email, first_name=first_name,last_name=last_name,picture=picture,activated=(activated == 'True'),gender=gender)
		tourist.put()
		return tourist

	@staticmethod
	def updateTourist(cls, email, first_name, last_name, country, state):
		cls.email = email
		cls.first_name = first_name
		cls.last_name = last_name
		cls.country = country
		cls.state = state
		cls.put()

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
