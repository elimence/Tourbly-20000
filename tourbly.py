
import webapp2
import logging
from security import Root


# ERROR HANDLERS

from errors import error_404
from errors import error_500


# IMPORT CONTROLLERS

from controllers import home
from controllers import guide
from controllers import image
from controllers import oauth
from controllers import signin
from controllers import signup
from controllers import logout
from controllers import loader
from controllers import places
from controllers import search
from controllers import profile
from controllers import add_place
from controllers import add_guide
from controllers import add_review
from controllers import verifyemail

# APPLICATION ENTRY

class tourbly(Root.Handler):
    def get(self):
        self.redirect('home')


# URI ROUTING

app = webapp2.WSGIApplication([
    webapp2.Route(r'/',                         handler=tourbly,                    name='root'),
    webapp2.Route(r'/home',                     handler=home.Home,                  name='home'),
    webapp2.Route(r'/img',                      handler=image.Image,                name='images'),
    webapp2.Route(r'/signin',                   handler=signin.Signin,              name='signin'),
    webapp2.Route(r'/signup',                   handler=signup.Signup,              name='signup'),
    webapp2.Route(r'/logout',                   handler=logout.Logout,              name='logout'),
    webapp2.Route(r'/places',                   handler=places.Places,              name='places'),
    webapp2.Route(r'/search',                   handler=search.Search,              name='search'),
    webapp2.Route(r'/profile',                  handler=profile.Profile,            name='profile'),
    webapp2.Route(r'/verify_email',             handler=verifyemail.VerifyEmail,    name='verify'),
    webapp2.Route(r'/guides/<:[0-9]+>',         handler=guide.GuideHandler,         name='guide'),
    webapp2.Route(r'/guides/apply',             handler=guide.GuideApplicationForm, name='guides_apply'),
    webapp2.Route(r'/oauth/<:[a-zA-Z]+>',       handler=oauth.Oauth,                name='oauth'),
    webapp2.Route(r'/loader',                   handler=loader.Loader,              name='loader'),
    webapp2.Route(r'/admin/guides/add_guide',   handler=add_guide.AddGuide,         name='add_guide'),
    webapp2.Route(r'/admin/places/add_place',   handler=add_place.AddPlace,         name='add_place'),
    webapp2.Route(r'/admin/reviews/add_review', handler=add_review.AddReview,       name='add_review'),
    webapp2.Route(r'/showplaceprofile',         handler=places.ShowPlace,           name='place_profile')


], debug=True)          # CHANGE TO False BEFORE FINAL DEPLOYMENT

# ERROR HANDLERS
app.error_handlers[404] = error_404.handle_404
app.error_handlers[500] = error_500.handle_500
