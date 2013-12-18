from security import Root
from models import Destination
from google.appengine.ext import db

class AddPlace(Root.Handler):
	def get(self):
		self.render("add_place.html")

	def post(self):
		destination_name = self.request.get("destination_name")
		country = "Ghana"
		region = "Ashanti"
		city = "Bonwire"
		tagline = self.request.get("tag_line")
		picture = self.request.get("picture")
		description = self.request.get("description")
		latlng = "1, -1"
		destination_tags = self.request.get("tags")
		direction = self.request.get("direction")

		tags = destination_tags.split(",")

		value_args = {"destination_name" : destination_name, "country" : country, "region" : region,
		"city" : city, "tagline" : tagline, "picture" : picture, "description" : description,
		"latlng" : latlng, "tags" : destination_tags}

		if destination_name and latlng and description:
			place = Destination.Destination(name = destination_name, country = country, region = region,
				city = city, tagline = tagline, picture_urls = [picture], description = description, latlng = latlng,
				tags = tags, direction = direction)
			place.put()
			self.redirect("/admin/places/add_place")
		else:
			self.render("add_place.html", value_args = value_args)

		