
from security import Root
from models import Tourist
from models import Guide
from google.appengine.api import urlfetch


class Image(Root.Handler):
    def get(self):
        entity_id = int(self.request.get('entity_id'))
        model = self.request.get("model")

        if model == "Guide":
        	entity = Guide.Guide.get_by_id(entity_id)
        elif model == "Tourist":
        	entity = Tourist.Tourist.get_by_id(entity_id)
        elif model == "Place":
            entity = Destination.Destination.get_by_id(entity_id)
        if entity.picture:
        	# picture = urlfetch.Fetch(entity.picture).content
        	self.response.headers['Content-Type'] = 'image/png'
        	self.write(entity.picture)
