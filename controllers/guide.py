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
    def get(self, guide_id):
    	guide = Guide.Guide.get_by_id(int(guide_id))

        if self.check_session("query"):
            tourist = Tourist.Tourist.get_by_id(self.get_user_id())
            self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"), tourist = tourist)
        else:
            self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"))

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
    		self.redirect("/guides/" + guide_id)
    	else:
    		self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"), tourist = tourist,
    			error = reviewing_error_prompt(name, comments), comments = comments, name = name)

class GuideApplicationForm(Root.Handler):
    def get(self):
        self.render("guide_signup_form.html")