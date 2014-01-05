from security import Root
from models import Guide
from models import Tourist
from models import Review

def reviewing_error_prompt(name, comments):
	if name == "":
		return "Please enter your name"
	elif comments == "":
		return "You need to comment before reviewing"

class GuideHandler(Root.Handler):
    def get(self, guide_id, place_id):
    	guide = Guide.Guide.get_by_id(int(guide_id))

        if self.check_session("query"):
            tourist = Tourist.Tourist.get_by_id(self.get_user_id())
            self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"), tourist = tourist,
                place_id = place_id)
        else:
            self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"), place_id = place_id)

    def post(self, guide_id, place_id):
    	guide = Guide.Guide.get_by_id(int(guide_id))
    	tourist = Tourist.Tourist.get_by_id(self.get_user_id())

    	if tourist.first_name:
    		name = tourist.first_name
    	else:
    		name = self.request.get("name")
        rating   = int(self.request.get("rating"))
    	comments = self.request.get("comment")

    	_args = {"name" : name, "comments" : comments}
    	if name and comments:
    		tourist.first_name = name
    		tourist.put()

    		review = Review.Review(_reviewer = tourist, _reviewee = guide, _comment = comments, _rating = rating)
    		review.put()
    		self.redirect("/guides/" + guide_id + "/"+ place_id)
    	else:
    		self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"), tourist = tourist,
    			error = reviewing_error_prompt(name, comments), comments = comments, name = name)




class GuideApplicationForm(Root.Handler):
    def get(self):
        countries = self.all_countries
        guide_details = {}
        self.render("guide_signup.html", isLoggedIn = self.check_session("query"), countries = countries,
            guide_details = guide_details)


    def post(self):
        countries = self.all_countries
        full_name = self.request.get("full_name")
        country = self.request.get("country")
        email = self.request.get("email")

        guide_details = {"full_name" : full_name, "country" : country, "email" : email}

        if full_name and country and email:
            if self.validate_email(email):
                _args = {"email" : email, "full_name" : full_name}
                self.send_guide_application_email(_args)
                self.redirect("/home")
            else:
                self.render("guide_signup.html", countries = countries, guide_details = guide_details,
                    email_error = "Invalid email entered")
        else:
            # self.write(country)
            self.render("guide_signup.html", countries = countries, guide_details = guide_details,
                error = "All fields are required")

class GuideViewHandler(Root.Handler):
    def get(self, guide_id):
        guide = Guide.Guide.get_by_id(int(guide_id))

        if self.check_session("query"):
            tourist = Tourist.Tourist.get_by_id(self.get_user_id())
            self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"), tourist = tourist, 
                isViewing = True)
        else:
            self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"), isViewing = True)

    def post(self, guide_id):
        guide = Guide.Guide.get_by_id(int(guide_id))
        tourist = Tourist.Tourist.get_by_id(self.get_user_id())

        if tourist.first_name:
            name = tourist.first_name
        else:
            name = self.request.get("name")
        rating   = int(self.request.get("rating"))
        comments = self.request.get("comment")

        _args = {"name" : name, "comments" : comments}
        if name and comments:
            tourist.first_name = name
            tourist.put()

            review = Review.Review(_reviewer = tourist, _reviewee = guide, _comment = comments, _rating = rating)
            review.put()
            self.redirect("/guides/" + guide_id + "/"+ place_id)
        else:
            self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"), tourist = tourist,
                error = reviewing_error_prompt(name, comments), comments = comments, name = name)
        
