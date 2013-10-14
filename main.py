
import webapp2

from models import Destination
from security import Root


class MainHandler(Root.Handler):
    def get(self):
        self.redirect('/home')

class HomeHandler(Root.Handler):
    def get(self):
        self.render("index.html")

class SignupHandler(Root.Handler):
    def get(self):
        self.render("signup.html")

    def post(self):
        

class SigninHandler(Root.Handler):
    def get(self):
        self.render("signin.html")

class PlacesHandler(Root.Handler):
    def get(self):
        places = Destination.Destination.getAllDestination()
        self.render("places.html", places = places)
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', HomeHandler),
    ('/signup', SignupHandler),
    ('/signin', SigninHandler),
    ('/places', PlacesHandler)
], debug=True)