
from security import Root
from models import Tourist
from models import Guide
from google.appengine.api import urlfetch
from google.appengine.api import files


class Image(Root.Handler):
    def get(self):
        entity_id = int(self.request.get('entity_id'))
        model = self.request.get("model")

        entity = Tourist.Tourist.get_by_id(entity_id)
        if entity.picture:
        	self.response.headers['Content-Type'] = 'image/png'
        	self.write(entity.picture)

class ReadCloudImage(Root.Handler):
	def get(self, tourist_id):
		BUCKET_BASE = "/gs/tourbly/profile_pictures/"

		with files.open(BUCKET_BASE + str(tourist_id), 'r') as fp:
			buf = fp.read(1000000)
			while buf:
				self.response.headers['Content-Type'] = 'image/png'
				self.write(buf)
				buf = fp.read(1000000)
		
		
