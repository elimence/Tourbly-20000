
import webapp2

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import mail
from google.appengine.ext import db
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
                hashed_password, salt = self.hash_password(_args)
                token, salt2 = self.hash_password(_args)
                tourist = Tourist.Tourist.addTourist(email, hashed_password, salt, token)

                session_vars = {"name" : "authenticator", "value" : email}
                self.create_session(session_vars)

                ph = "lkdsjfdsjklfjhiwereyim,nn.nafndfgityereryewiybx,ncn,neroejslfjoiuer"
                _args = {"name":email + ph, "password":password}
                verification_link = "http://tourbly.appspot.com/verify_email?token=" + token + "&email=" + email
                params = {"email" : email, "url" : verification_link}
                self.send_verification_email(params)
                self.render("home.html", test = "Signed up successfully, " + tourist.email)
            else:
                self.render("signup.html", email = email, email_error = self.email_error_prompt(email), password_error = self.password_error_prompt(password), confirm_password_error = self.confirm_password_error_prompt(password, confirm_password))
        else:
            error = "All fields are required"
            self.render("signup.html", email = email, error = error)


class SigninHandler(Root.Handler):
    def get(self):
        self.render("signin.html")

    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")
        all_users = Tourist.Tourist.all()
        # tourist = self.get_user_by_email(all_users, email)
        tourist = db.GqlQuery("select * from Tourist where email = :1", email).get()

        if email and password:
            if tourist:
                hashed_password= tourist.password
                salt = tourist.salt
                _args = {"password" : password, "hashed_password" : hashed_password, "salt" : salt}
                if self.auth_password(_args):
                    session_vars = {"name" : "authenticator", "value" : email}
                    self.create_session(session_vars)

                    if tourist.firstName == None:
                        self.render("home.html", test = "You've been signed in successfully, " + tourist.email)
                    else:
                        self.render("home.html", test = "You've been signed in successfully, " + tourist.firstName)
                else:
                    self.render("signin.html", error = "Invalid email or password")
            else:
                self.render("signin.html", error = "User with email " + email + " cannot be found")
        else:
            self.render("signin.html", error = "Both fields are required")

class PlacesHandler(Root.Handler):
    def get(self):
        places = Destination.Destination.getAllDestination()
        self.render("places.html", places = places)  

class LogoutHandler(Root.Handler):
     def get(self):
        self.logout(["authenticator"])

class VerifyEmailhandler(Root.Handler):
    def get(self):
        token = self.request.get("token")
        email = self.request.get("email")
        tourist = db.GqlQuery("select * from Tourist where email = :1", email).get()

        if tourist.token == token:
            tourist.activated = True
            tourist.put()
            self.render("home.html", test = "Your account has been activated")
        else: 
            self.redirect("/home")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', HomeHandler),
    ('/signup', SignupHandler),
    ('/signin', SigninHandler),
    ('/places', PlacesHandler),
    ('/logout', LogoutHandler),
    ('/verify_email', VerifyEmailhandler)
  
], debug=True)