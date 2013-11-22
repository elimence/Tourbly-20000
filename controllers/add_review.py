from security import Root		

class AddReview(Root.Handler):		
	def get(self):
		self.render("add_review.html")
		