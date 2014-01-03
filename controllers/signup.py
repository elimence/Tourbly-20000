
from security import Root
from models import Tourist
from google.appengine.api import urlfetch
import urllib
import logging


class Signup(Root.Handler):
    def get(self):
        referer = self.request.referer
        if referer:
            referer = referer[referer.find("/", 8) : ]
        if self.check_session("query"):
            self.redirect("/home")
        else:
            self.render("signup.html", isLoggedIn = self.check_session("query"), referer = referer)

    def post(self):
        referer = self.request.get("referer")
        if referer == 'None':
            referer = '/home'

        redirects = self.get_cookie("redirects")

        email = self.request.get("email")
        password = self.request.get("password")
        confirm_password  = self.request.get("confirm_password")
        # picture_fetch = urlfetch.Fetch("http://s3.amazonaws.com/37assets/svn/765-default-avatar.png")
        # picture = picture_fetch.content
        picture = "http://s3.amazonaws.com/37assets/svn/765-default-avatar.png"
        all_users = Tourist.Tourist.all()

        if email and password and confirm_password:
            if self.validate_email(email) and self.validate_password(password) and password == confirm_password and (self.get_user_by_email(all_users, email) == None):
                # tourist_obj = Tourist.Tourist(username = username, password = password, email = email)
                _args = {"name":email, "password":password}
                hashed_password, salt = self.hash_password(_args)
                token, salt2 = self.hash_password(_args)
                tourist = Tourist.Tourist.addTourist(email, hashed_password, salt, token, picture)

                session_vars = {"name" : "authenticator", "value" : email}
                session_vars2 = {"name" : "query", "value" : tourist.key().id()}
                self.create_session(session_vars)
                self.create_session(session_vars2)

                ph = "lkdsjfdsjklfjhiwereyim,nn.nafndfgityereryewiybx,ncn,neroejslfjoiuer"
                _args = {"name":email + ph, "password":password}
                verification_link = "http://gcdc2013-tourbly.appspot.com/verify_email?token=" + token + "&id=" + str(tourist.key().id())
                params = {"email" : email, "url" : verification_link}
                self.send_verification_email(params)

                if redirects[0] is not None:
                    redirects = urllib.unquote(redirects[0].decode("utf-8"))
                    redirects = redirects[redirects.find("/", 8) : ]

                    self.delete_cookie("redirects")
                    self.redirect(redirects)
                elif referer == "/home":
                    self.redirect("/search")
                else:
                    self.redirect(referer)
            else:
                self.render("signup.html", email = email, email_error = self.email_error_prompt(email),
                    password_error = self.password_error_prompt(password), confirm_password_error =
                    self.confirm_password_error_prompt(password, confirm_password))
        else:
            error = "All fields are required"
            self.render("signup.html", email = email, error = error)



class Switch(Root.Handler):
    def post(self):
        password = self.request.body
        tourist_id = int(self.get_cookie("query")[0])
        tourist = Tourist.Tourist.get_by_id(tourist_id)

        _args = {"name":tourist.email, "password":password}
        hashed_password, salt = self.hash_password(_args)
        token, salt2 = self.hash_password(_args)

        tourist.password = hashed_password
        tourist.salt = salt
        tourist.token = token
        tourist.acct_type = 'regular'
        res = tourist.put()
        self.write(res)


