
import logging
from security import Root
from models import Tourist


class OrderConfirmation(Root.Handler):
	def get(self):
		if self.check_session("query"):
			tourist_id = int(self.get_cookie("query")[0])
			tourist = Tourist.Tourist.get_by_id(tourist_id)
			booking_number = self.request.get("booking_number")

			if not self.request.get('price'):
				self.redirect('/home')
			else:
				self.render("order_confirmation.html", isLoggedIn = self.check_session("query"), tourist = tourist,
					arrival=self.request.get('arrival'), departure=self.request.get('departure'), price=self.request.get('price'),
					duration=self.request.get('duration'), guideName=self.request.get('guideName'),
					placeName=self.request.get('placeName'), bookingNumber=booking_number)
		else:
			self.redirect("/home")


	def post(self):
		if self.check_session("query"):
			tourist_id = int(self.get_cookie("query")[0])
			tourist = Tourist.Tourist.get_by_id(tourist_id)
			booking_number = tourist.email[1:3] + '-' + str(hash(tourist.email))[-4:]

			arrival = arrival=self.request.get('arrival')
			departure=self.request.get('departure')
			price=self.request.get('price')
			duration=self.request.get('duration')
			guideName=self.request.get('guideName')
			placeName=self.request.get('placeName')

			self.redirect("/booking/confirm?arrival=" + arrival + "&departure=" + departure + "&price=" + price + "&duration="
				+ duration + "&guideName=" + guideName + "&placeName=" + placeName + "&booking_number=" + booking_number)
		else:
			self.redirect("/home")
