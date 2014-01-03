import logging
from security import Root

class Pay(Root.Handler):
	def get(self):
		self.render("wallet-demo.html")

	def post(self):
		logging.info("Post called By Google, Hurray!")

