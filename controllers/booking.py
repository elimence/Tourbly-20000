# @Sam / @Chris: I created this file only to help me render the booking page
# Feel free to edit and add functionality as needed
from security import Root
from models import Guide
from models import Tourist
from models import Review
from models import Destination
from datetime import datetime

# def getNumberOfDays(arrival, departure):


class BookingHandler(Root.Handler):
	def get(self, guide_id, place_id):
		guide = Guide.Guide.get_by_id(int(guide_id))
		place = Destination.Destination.get_by_id(int(place_id))

	  	countries = self.all_countries
	  	country = self.request.get("country")
	  	arrival = self.request.get("arrival")
	  	departure = self.request.get("departure")

	  	date_format = "%d %MM, %yyyy"
	  	# arrival_date = date.strptime(arrival, date_format)
	  	# departure_date = date.strptime(departure, date_format)
	  	# tour_days = (arrival_date - departure_date).days

	  	booking_args = {"country" : country, "arrival" : arrival, "departure" : departure, "tour_days" : 2}

	  	if self.check_session("query"):
	  		self.render("booking.html", isLoggedIn = self.check_session("query"), countries = countries,
                bookingArgs = booking_args, guide = guide, place = place, touristID=self.get_user_id())
	  	else:
	  		self.redirect("/home")


	def post(self):
		country = self.request.get("country")
		arrival = self.request.get("arrival")
		departure = self.request.get("departure")
		message = self.request.get("message")

class GuideAvailableHandler(Root.Handler):
	def get(self):
		guide_id = self.request.get("guide_id")
		start_date = self.request.get("start_date")
		end_date =  self.request.get("end_date")

		guide = Guide.Guide.get_by_id(int(guide_id))
		start_date = datetime.strptime(start_date, '%d %B, %Y')
		end_date = datetime.strptime(end_date, '%d %B, %Y')

		output = "false"
		for booking in guide.guide_booking_set:
			if (booking._tour_start <= end_date) and (start_date <= booking._tour_end):
				output = "true"
				break

		self.write(output)



		
		

