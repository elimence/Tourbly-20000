from google.appengine.ext import db

class Tourist(db.Model):
	firstName = db.StringProperty()
	lastName = db.StringProperty()
	email = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	country = db.StringProperty()
	state = db.StringProperty()
	languages = db.ArrayProperty()
	picture = db.BlobProperty()

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

	
