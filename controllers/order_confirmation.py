
import logging
from security import Root
from models import Tourist


class OrderConfirmation(Root.Handler):
	def post(self):
		if self.check_session("query"):
			tourist_id = int(self.get_cookie("query")[0])
			tourist = Tourist.Tourist.get_by_id(tourist_id)
			booking_number = tourist.first_name[1:2] + tourist.last_name[1:2] + '-' + str(hash(tourist.email))[:-4]

			self.render("order_confirmation.html", isLoggedIn = self.check_session("query"), tourist = tourist,
				arrival=self.request.get('arrival'), departure=self.request.get('departure'), price=self.request.get('price'),
				duration=self.request.get('duration'), guideName=self.request.get('guideName'),
				placeName=self.request.get('placeName'), bookingNumber=booking_number)
		else:
			self.redirect("/home")
