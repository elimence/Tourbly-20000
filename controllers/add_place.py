from security import Root

class AddPlace(Root.Handler):
	def get(self):
		self.render("add_place.html")
		