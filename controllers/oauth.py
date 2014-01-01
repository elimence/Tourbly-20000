
import logging
import urllib

from security import Root
from models import Tourist
from google.appengine.ext import db

class Oauth(Root.Handler):
    def get(self):
        pass

    def post(self):
        # Get all Tourists from db
    	all_users 	= Tourist.Tourist.all()

        # Get Tourist details from request object
    	email 		= self.request.get('email')
    	activated 	= self.request.get('activated')
        first_name 	= self.request.get('first_name')
        last_name 	= self.request.get('last_name')
        gender 		= self.request.get('gender')
        picture 	= self.request.get('picture')


        # Attempt to retrieve Tourist
        tourist = self.get_user_by_email(all_users, email)

        # If Tourist doesn't exist, create new Tourist
        if tourist == None:
            tourist = Tourist.Tourist.create_from_oauth(email, first_name, last_name, gender, picture, activated)

        session_vars = {'name': 'authenticator', 'value': email, "validity" : 4}
        session_vars2 = {"name" : "query", "value" : tourist.key().id(), "validity" : 4}

        # Create auth cookies for Tourist
        cookie_str1 = self.create_cookie_str(session_vars)
        cookie_str2 = self.create_cookie_str(session_vars2)

        # Set auth cookies and grant access
        self.write(cookie_str1+"*-*"+cookie_str2)



class CloseAccount(Root.Handler):
    def get(self):
        pass
    def post(self):
        logging.info("inside disconnet's post")
        tourist_id = int(self.get_cookie("query")[0])
        tourist = Tourist.Tourist.get_by_id(tourist_id)
        db.delete(tourist)
        self.write("deleted")




