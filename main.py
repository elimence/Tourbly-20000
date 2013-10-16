
import webapp2

from models import Destination, Tourist, Guide, Request
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
        email = self.request.get("email")
        password = self.request.get("password")
        confirm_password  = self.request.get("confirm_password")
        all_users = Tourist.Tourist.all()

        if email and password and confirm_password:
            if self.validate_email(email) and self.validate_password(password) and password == confirm_password and (self.get_user_by_email(all_users, email) == None):
                # tourist_obj = Tourist.Tourist(username = username, password = password, email = email)
                _args = {"name":email, "password":password}
                hashed_password = self.hash_password(_args)
                tourist = Tourist.Tourist.addTourist(email, hashed_password)
                self.render("home.html", test = "Signed up successfully, " + tourist.email)
            else:
                self.render("signup.html", email = email, email_error = self.email_error_prompt(email), password_error = self.password_error_prompt(password), confirm_password_error = self.confirm_password_error_prompt(password, confirm_password))
        else:
            error = "All fields are required"
            self.render("signup.html", email = email, error = error)


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