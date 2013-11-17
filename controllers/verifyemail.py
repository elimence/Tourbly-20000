from security import Root


class VerifyEmail(Root.Handler):
    def get(self):
        token = self.request.get("token")
        tourist_id = int(self.request.get("id"))
        tourist = Tourist.Tourist.get_by_id(tourist_id)

        if tourist.token == token:
            tourist.activated = True
            tourist.put()
            self.render("profile.html", success_message = "Your account has been activated")
        else:
            self.redirect("/home")
