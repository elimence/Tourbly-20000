from security import Root
from models import Guide
from datetime import datetime

class AddGuide(Root.Handler):
	def get(self):
		self.render("add_guide.html", isLoggedIn = self.check_session("query"), countries = self.all_countries)

	def post(self):
		firstname = self.request.get("first_name")
		lastname = self.request.get("last_name")
		email = self.request.get("email")
		country = self.request.get("country")
		state = self.request.get("state")
		picture = self.request.get("picture")
		dob = self.request.get("dob")
		email = self.request.get("email")
		phoneNumber = self.request.get("phone_number")
		languages = self.request.get("languages")
		elevator_pitch = self.request.get("elevator_pitch")
		gender = self.request.get("gender")

		dateOfBirth = datetime.strptime(dob, "%d %B, %Y")

		if country:
			guide = Guide.Guide(_firstname = firstname, _lastname = lastname, _email = email, _country = country,
				_lives_in = state, _phoneNumber = phoneNumber, _gender = gender, _picture = picture, _dateOfBirth
				= dateOfBirth, _languages = languages.split(","), _elevator_pitch = elevator_pitch)

			guide.put()
		self.redirect("/admin/guides/add_guide")
