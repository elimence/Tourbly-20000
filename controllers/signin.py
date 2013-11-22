
import logging
from security import Root
from models import Tourist
from google.appengine.ext import db


class Signin(Root.Handler):
    def get(self):
        if self.check_session("query"):
            self.redirect("/home")
        else:
            self.render("signin.html", isLoggedIn = self.check_session("query"))

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
                    session_vars2 = {"name" : "query", "value" : tourist.key().id()}
                    self.create_session(session_vars)
                    self.create_session(session_vars2)

                    self.redirect('/search')
                    # if tourist.first_name == None:
                    #     self.render("home.html", test = "You've been signed in successfully, " + tourist.email)
                    # else:
                    #     self.render("home.html", test = "You've been signed in successfully, " + tourist.first_name)
                else:
                    self.render("signin.html", error = "Invalid email or password")
            else:
                self.render("signin.html", error = "User with email " + email + " cannot be found")
        else:
            self.render("signin.html", error = "Both fields are required")
