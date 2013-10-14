from google.appengine.ext import db

class Tourist(db.Model):
	firstName = db.StringProperty()
	lastName = db.StringProperty()
	email = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	country = db.StringProperty()
	state = db.StringProperty()
	languages = db.ListProperty(String)
	picture = db.BlobProperty()
	created = db.DateTimeProperty(auto_now_add = True)

	@classmethod
	def addTourist(cls, email, password):
		hashed_password = Helper.make_pw_hash(password)

		if email and hashed_password:
			all_users = cls.all()
			check_user = Helper.checkUserExists(all_users, email)

			if check_user:
				return False, check_user
			else:
				tourist = cls(email = email, password = hashed_password)
				tourist.put()
				return True, tourist

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
