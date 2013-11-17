from security import Root



class Profile(Root.Handler):
    def get(self):
        if self.check_session("query"):
            tourist_id = int(self.get_cookie("query")[0])
            tourist = Tourist.Tourist.get_by_id(tourist_id)
            self.render("profile.html", email = tourist.email, first_name = tourist.first_name,
                last_name = tourist.last_name, country = tourist.country, state = tourist.state,
                tourist_id = tourist_id, isLoggedIn = self.check_session("query"), tourist = tourist)
        else:
            self.redirect("/home")

    def post(self):
        tourist_id = int(self.get_cookie("query")[0])
        tourist = Tourist.Tourist.get_by_id(tourist_id)

        new_email = self.request.get("email")
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        country = self.request.get("country")
        state = self.request.get("state")
        picture = self.request.get("profile_pic")

        if self.validate_email(new_email) and self.validate_name(first_name) and self.validate_name(last_name):
            Tourist.Tourist.updateTourist(tourist, new_email, first_name, last_name, country, state)
            if picture:
                tourist.picture = str(picture)
                tourist.put()
            self.render("profile.html", email = tourist.email, first_name = tourist.first_name,
                last_name = tourist.last_name, country = tourist.country, state = tourist.state, isLoggedIn = self.check_session("query"),
                tourist_id = tourist_id, success_message = "Your profile has been updated successfully", tourist = tourist)
        else:
            self.render("profile.html", email = new_email, email_error = self.profile_email_error_prompt(tourist.email, new_email), first_name =
                first_name, last_name = last_name, state = state, tourist_id = tourist_id, success_message = "there is something wrong")
