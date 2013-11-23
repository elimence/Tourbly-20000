from security import Root		
from models import Tourist
from models import Guide

class AddReview(Root.Handler):		
	def get(self):
		self.render("add_review.html")

	def post(self):
		reviewer_id = self.request.get("reviewer_id")
		reviewee_id = self.request.get("reviewee_id")
		rating = self.request.get("rating")
		review = self.request.get("review")

		reviewer = Tourist.Tourist.get_by_id(reviewer_id)
		reviewee = Guide.Guide.get_by_id(reviewee_id)

		if reviewer and reviewee and rating and review:
			review = Review.Review(_reviewer = reviewer, _reviewee = reviewee, _rating = rating, _comment = review)
			review.put()

			self.redirect("/admin/reviews/add_review")
		self.render("add_review.html")
		