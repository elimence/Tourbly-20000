from security import Root
from models import Destination
from google.appengine.ext import db

from google.appengine.api import urlfetch
import urllib
import json

class AddPlace(Root.Handler):
	def get(self):
		self.render("add_place.html")

	def post(self):
		destination_name = self.request.get("destination_name")
		destination_map_name = self.request.get("map_name")
		country = ""
		region = ""
		city = ""
		tagline = self.request.get("tag_line")
		picture = self.request.get("picture")
		description = self.request.get("description")
		latlng = ""
		destination_tags = self.request.get("tags")
		direction = self.request.get("direction")

		tags = destination_tags.split(",")
		
		if destination_map_name:
			request = urlfetch.Fetch("https://maps.googleapis.com/maps/api/geocode/json?address="
				+ urllib.quote(destination_map_name.encode("utf-8")) + "&sensor=true").content

			request_json = json.loads(request)
			country = self.getCountryFromJson(request_json)
			region = self.getRegionFromJson(request_json)
			city = self.getCityFromJson(request_json)
			latlng = self.getLatLngFromJson(request_json)

		value_args = {"destination_name" : destination_name, country : country, "region" : region,
		"city" : city, "tagline" : tagline, "picture" : picture, "description" : description,
		"latlng" : latlng, "tags" : destination_tags, "map_name" : destination_map_name }
		if destination_name and latlng and description:
			place = Destination.Destination(name = destination_name, country = country, region = region,
				city = city, tagline = tagline, pictures = [picture], description = description, latlng = latlng,
				tags = tags, direction = direction)
			place.put()
			self.redirect("/admin/places/add_place")
		else:
			self.render("add_place.html", value_args = value_args)

		