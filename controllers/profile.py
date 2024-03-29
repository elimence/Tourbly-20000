
import logging
from security import Root
from models import Tourist
from google.appengine.api import files

try:
    files.gs
except AttributeError:
    import gs
    files.gs = gs

class Profile(Root.Handler):
    def get(self):
        countries = self.all_countries

        if self.check_session("query"):
            tourist_id = int(self.get_cookie("query")[0])
            tourist = Tourist.Tourist.get_by_id(tourist_id)

            profile_args = {"email" : tourist.email, "country" : tourist.country, "first_name" : tourist.first_name, 
            "last_name" : tourist.last_name, "state" : tourist.state, "picture" : tourist.picture}

            googleAccount = True if tourist.acct_type == "google" else False

            self.render("profile.html", isLoggedIn = self.check_session("query"), tourist = tourist,
                googleAccount = googleAccount, countries = countries, profile_args = profile_args)
        else:
            self.redirect("/home")

    def post(self):
        countries = self.all_countries
        tourist_id = int(self.get_cookie("query")[0])
        tourist = Tourist.Tourist.get_by_id(tourist_id)

        new_email = self.request.get("email")
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        country = self.request.get("country")
        state = self.request.get("state")
        picture = self.request.POST.get("photo")
        # self.write(picture.filename[picture.filename.find(".") + 1 : ])

        profile_args = {"email" : new_email, "country" : country, "first_name" : first_name, 
            "last_name" : last_name, "state" : state, "picture" : picture}

        if self.validate_email(new_email) and self.validate_name(first_name) and self.validate_name(last_name):
            Tourist.Tourist.updateTourist(tourist, new_email, first_name, last_name, country, state)
            if picture != None and picture != "":
                picture_extension = picture.filename[picture.filename.rfind(".") : ]
                picture_url = "/tourbly/profile_pictures/" +  str(tourist.key().id()) + self.rand_salt("picture") + picture_extension
                picture_name = "/gs" + picture_url
                writable_file_name = files.gs.create(picture_name, mime_type='image/jpeg', acl='public-read')
                with files.open(writable_file_name, 'a') as f:
                    f.write(picture.file.read())
                files.finalize(writable_file_name)

                tourist.picture = "http://storage.googleapis.com" + picture_url
                tourist.put()
            self.render("profile.html", isLoggedIn = self.check_session("query"), profile_args = profile_args,
                success_message = "Your profile has been updated successfully", tourist = tourist, 
                countries = countries)
        else:
            self.render("profile.html", email_error = self.profile_email_error_prompt(tourist.email, new_email),
             profile_args = profile_args, success_message = "there is something wrong", countries = countries)


class UploadAndReadImageHandler(Root.Handler):
    def post(self):
        picture = self.request.POST.get("photo")

        if picture != None:
                picture_extension = picture.filename[picture.filename.find(".") + 1 : ]
                picture_name = "/gs/tourbly/profile_pictures" +  str(tourist.key().id()) + picture_extension
                writable_file_name = files.gs.create(picture_name, mime_type='image/jpeg', acl='public-read')
                with files.open(writable_file_name, 'a') as f:
                    f.write(picture.file.read())
                files.finalize(writable_file_name)

                with files.open(picture_name, 'r') as fp:
                    buf = fp.read(1000000)
                    while buf:
                        self.response.headers['Content-Type'] = 'image/png'
                        self.write(buf)
                        buf = fp.read(1000000)
        
        




