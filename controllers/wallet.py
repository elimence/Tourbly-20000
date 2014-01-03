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
import logging

# application-specific imports
from sellerinfo import SELLER_ID
from sellerinfo import SELLER_SECRET

class Wallet(webapp.RequestHandler):
  def get(self, duration):

    price = int(duration) * 50
    curr_time = int(time.time())
    exp_time = curr_time + 3600
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
        "sellerData" : "user_id:1224245,offer_code:3098576987,affiliate:aksdfbovu9j"
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


