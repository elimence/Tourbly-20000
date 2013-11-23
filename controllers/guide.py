from security import Root
from models import Guide
from models import Tourist

class GuideHandler(Root.Handler):
    def get(self, guide_id):
    	guide = Guide.Guide.get_by_id(int(guide_id))

        if self.check_session("query"):
            tourist = Tourist.Tourist.get_by_id(self.get_user_id())
            self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"), tourist = tourist)
        else:
            self.render("guide.html", guide = guide, isLoggedIn = self.check_session("query"))
