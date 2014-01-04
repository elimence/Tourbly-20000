
from security import Root
from models import Tourist
from models import Guide
from google.appengine.api import urlfetch


class Image(Root.Handler):
    def get(self):
        entity_id = int(self.request.get('entity_id'))
        model = self.request.get("model")

        entity = Tourist.Tourist.get_by_id(entity_id)
        if entity.picture:
        	self.response.headers['Content-Type'] = 'image/png'
        	self.write(entity.picture)

# class ReadCloudImage(Root.Handler):
# 	def get(self):
		
		
