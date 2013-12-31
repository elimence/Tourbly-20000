
import logging
import urllib

from security import Root
from models import Tourist

class Oauth(Root.Handler):
    def get(self):
        pass

    def post(self, dest):
    	all_users 	= Tourist.Tourist.all()
    	email 		= self.request.get('email')
    	activated 	= self.request.get('activated')

        if dest == 'signup':


	        first_name 	= self.request.get('first_name')
	        last_name 	= self.request.get('last_name')
	        gender 		= self.request.get('gender')
	        picture 	= self.request.get('picture')



	        if self.get_user_by_email(all_users, email) == None:
	        	tourist = Tourist.Tourist.create_from_oauth(email, first_name, last_name, gender, picture, activated)
	        	session_vars = {'name': 'authenticator', 'value': email, "validity" : 4}
	        	session_vars2 = {"name" : "query", "value" : tourist.key().id(), "validity" : 4}

	        	# self.create_session(session_vars)
	        	# self.create_session(session_vars2)
	        	cookie_str1 = self.create_cookie_str(session_vars)
	        	cookie_str2 = self.create_cookie_str(session_vars2)

	        	self.write(cookie_str1+"*-*"+cookie_str2)

	        else:
	        	self.write('duplicate')


    	else:
    		tourist 	= self.get_user_by_email(all_users, email)
    		logging.info(tourist)
    		logging.info('email')
    		logging.info(email)

    		if tourist == None:
    			self.write('notfound')

    		else:

    			session_vars = {'name': 'authenticator', 'value': email, "validity" : 4}
    			session_vars2 = {"name" : "query", "value" : tourist.key().id(), "validity" : 4}

    			cookie_str1 = self.create_cookie_str(session_vars)
    			cookie_str2 = self.create_cookie_str(session_vars2)

    			self.write(cookie_str1+"*-*"+cookie_str2)
