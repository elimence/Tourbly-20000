from google.appengine.ext import db

class Helper(db.model):
	@staticmethod
    def make_salt():
        return ''.join(random.choice(string.letters) for i in range(5))

    def make_pw_hash(password):
        salt = Utilities.make_salt()
        pw_hash = password + salt
        return hashlib.sha256(pw_hash).hexdigest() + salt, salt

    @staticmethod
    def check_pw_hash(password, user):
        pw_hash = password + user.salt
        hashed = hashlib.sha256(pw_hash).hexdigest() + user.salt
        if hashed == user.password:
            return True
        else: return False

    @staticmethod
    def checkUserExists(all_users, email):
        return all_users.filter("email =", email).get()

    @staticmethod
    def verify_user(self, email, password, user_type):
    	all_users = null
    	if user_type == "tourist":
        	all_users = Tourist.all()
        else:
        	all_users = Guide.all()
        found_user = Helper.checkUserExists(all_users, email)
        
        if found_user:
            check_password = Helper.check_pw_hash(password, found_user)
            if check_password:
                return True, found_user
            else:
                return False, found_user
        
