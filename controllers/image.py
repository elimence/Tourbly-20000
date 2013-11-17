
from security import Root
from models import Tourist


class Image(Root.Handler):
    def get(self):
        tourist_id = int(self.request.get('tourist_id'))
        tourist = Tourist.Tourist.get_by_id(tourist_id)
        if tourist.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.write(tourist.picture)
