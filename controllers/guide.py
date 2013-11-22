from security import Root
from models import Guide

class GuideHandler(Root.Handler):
    def get(self, guide_id):
    	guide = Guide.Guide.get_by_id(int(guide_id))
    	# self.write(guide_id)
        self.render("guide.html", guide = guide)
