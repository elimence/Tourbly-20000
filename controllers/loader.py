from security import Root

class Loader(Root.Handler):
	def get(self):
		self.write("default db load will be here")
		