
import logging
from security import Root
from models import Tourist
from google.appengine.ext import db
import urllib


class Signin(Root.Handler):
    def get(self):
        referer = self.request.referer
        if referer:
            referer = referer[referer.find("/", 8) : ]
        if self.check_session("query"):
            self.redirect("/home")
        else:
            self.render("signin.html", isLoggedIn = self.check_session("query"), referer = referer)

    def post(self):
        referer = self.request.get("referer")
        redirects = self.get_cookie("redirects")

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

                    if redirects[0] is not None:
                        redirects = urllib.unquote(redirects[0].decode("utf-8"))
                        redirects = redirects[redirects.find("/", 8) : ]

                        self.redirect(redirects)
                    elif referer == "/home":
                        self.redirect("/search")
                    else:
                        self.redirect(referer)
                else:
                    self.render("signin.html", email = email, error = "Invalid email or password")
            else:
                self.render("signin.html", email = email, error = "User with email " + email + " cannot be found")
        else:
            self.render("signin.html", email = email, error = "Both fields are required")
