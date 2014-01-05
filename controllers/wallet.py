# Copyright 2012 Google Inc. All Rights Reserved.

# pylint: disable-msg=C6409,C6203

"""Wallet Subscriptions - Digital Content Subscriptions Python Sample"""

# standard library imports
from cgi import escape
import os
import time

# third-party imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import jwt
import json
import logging

from datetime import datetime

from models import Booking
from models import Guide
from models import Tourist
from models import Destination

# application-specific imports
from sellerinfo import SELLER_ID
from sellerinfo import SELLER_SECRET

class Wallet(webapp.RequestHandler):
  def get(self, duration):

    # Get entries for seller data object
    end = self.request.get('end') or ""
    start = self.request.get('start') or ""
    price = self.request.get('price') or ""
    guideID = self.request.get('guideID') or ""
    touristID = self.request.get('touristID') or ""
    paymentStatus = self.request.get('paymentStatus') or ""
    description = self.request.get('description') or ""
    message = self.request.get('message') or ""
    placeID = self.request.get('placeID') or ""

    price = int(duration) * 50
    curr_time = int(time.time())
    exp_time = curr_time + 3600


    sellerData = {
      "description":description,
      "guideID":guideID,
      "price":price,
      "paymentStatus":paymentStatus,
      "touristID":touristID,
      "start":start,
      "end":end,
      "message":message
    }

    logging.info(price)
    jwt_info = {
      "iss" : SELLER_ID,
      "aud" : 'Google',
      "typ" : 'google/payments/inapp/item/v1',
      "exp" : exp_time,
      "iat" : curr_time,
      "request" :{
        "name" : "Book a Tourbly Guide",
        "description" : 'One time payment for a '+ duration+ ' day guided tour',
        "price" : price,
        "currencyCode" : "USD",
        "sellerData" : json.dumps(sellerData)
      }
    }

    token = jwt.encode(jwt_info, SELLER_SECRET)
    self.response.write(token)



  def post(self):
    encoded_jwt = self.request.get('jwt', None)
    if encoded_jwt is not None:
      # jwt.decode won't accept unicode, cast to str
      # http://github.com/progrium/pyjwt/issues/4
      decoded_jwt = jwt.decode(str(encoded_jwt), SELLER_SECRET)

      # validate the payment request and respond back to Google
      if decoded_jwt['iss'] == 'Google' and decoded_jwt['aud'] == SELLER_ID:
        if ('response' in decoded_jwt and
            'orderId' in decoded_jwt['response'] and
            'request' in decoded_jwt):
          order_id = decoded_jwt['response']['orderId']
          request_info = decoded_jwt['request']
          if ('currencyCode' in request_info and 'sellerData' in request_info
              and 'name' in request_info and 'price' in request_info):
            # optional - update local database
            seller_dat = json.loads(request_info['sellerData'])

            # Get entries for seller data object
            end = datetime.strptime(str(seller_dat['end']), '%d %B, %Y')
            start = datetime.strptime(str(seller_dat['start']), '%d %B, %Y')
            price = str(seller_dat['price'])
            guide = Guide.Guide.get_by_id(int(seller_dat['guideID']))
            tourist = Tourist.Tourist.get_by_id(int(seller_dat['touristID']))
            paymentStatus = str(seller_dat['paymentStatus'])
            description = str(seller_dat['description'])
            message = str(seller_dat['message'])

            booking = Booking.Booking(_tourist=tourist, _guide=guide, _tour_start=start,
              _tour_end=end, _message=message, _description=description, _price=price,
               _payment_staus=paymentStatus, _booking_number=order_id)
            booking.put()

            email_args = {"email" : tourist.email, "booking_id" : order_id, "start_date" : start, "end_date": end, 
            "description" : description, "guide_firstname" : guide.first._firstname, "guide_lastname" : guide._lastname,
             "guide_number" : guide._phoneNumber, "guide_email" : guide.email, "price" : price}

            self.send_booking_email(email_args)

            # respond back to complete payment
            self.response.out.write(order_id)

        # check if this was a subscription cancellation postback
        if ('response' in decoded_jwt and
            'orderId' in decoded_jwt['response'] and
            'statusCode' in decoded_jwt['response']):
          status_code =  decoded_jwt['response']['statusCode']
          if status_code == 'SUBSCRIPTION_CANCELED':
            # process cancellation
            cancelled = 1


