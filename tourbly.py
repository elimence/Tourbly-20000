
import webapp2
import logging
from security import Root


# ERROR HANDLERS

from errors import error_404
from errors import error_500


# IMPORT CONTROLLERS

from controllers import home
from controllers import image
from controllers import signin
from controllers import signup
from controllers import logout
from controllers import places
from controllers import profile
from controllers import verifyemail



# APPLICATION ENTRY

class tourbly(Root.Handler):
    def get(self):
        self.redirect('/signin')


# URI ROUTING

app = webapp2.WSGIApplication([
    webapp2.Route(r'/',               handler=tourbly,                    name='root'),
    webapp2.Route(r'/home',           handler=home.Home,                  name='home'),
    webapp2.Route(r'/img',            handler=image.Image,                name='images'),
    webapp2.Route(r'/signin',         handler=signin.Signin,              name='signin'),
    webapp2.Route(r'/signup',         handler=signup.Signup,              name='signup'),
    webapp2.Route(r'/logout',         handler=logout.Logout,              name='logout'),
    webapp2.Route(r'/places',         handler=places.Places,              name='places'),
    webapp2.Route(r'/profile',        handler=profile.Profile,            name='profile'),
    webapp2.Route(r'/verify_email',   handler=verifyemail.VerifyEmail,    name='verify')

], debug=True)          # CHANGE TO False BEFORE FINAL DEPLOYMENT

# ERROR HANDLERS
app.error_handlers[404] = error_404.handle_404
app.error_handlers[500] = error_500.handle_500



