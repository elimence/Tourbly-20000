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

# application-specific imports
from sellerinfo import SELLER_ID
from sellerinfo import SELLER_SECRET

class Wallet(webapp.RequestHandler):
  """Handles /"""

  def get(self):
    """Handles get requests."""

    curr_time = int(time.time())
    exp_time = curr_time + 3600

    # subscription initial payment data
    initial_payment_info = {'price': '0.00',
                            'currencyCode': 'USD',
                            'paymentType': 'free_trial'}

    # subscription recurrence data
    recurrence_info = {'price': '1.99',
                       'currencyCode': 'USD',
                       'startTime': curr_time + 36000,
                       'frequency': 'monthly',
                       'numRecurrences': '12'}

    # subscription request object info
    request_info = {'sellerData': 'Custom Data',
                    'initialPayment': initial_payment_info,
                    'recurrence': recurrence_info}

    # common JWT
    jwt_info = {'iss': SELLER_ID,
                'aud': 'Google',
                'typ': 'google/payments/inapp/subscription/v1',
                'iat': curr_time,
                'exp': exp_time,
                'request': request_info}

    # create JWT for first subscription - free trial
    request_info.update({'name': 'Digital Posters - Free Trial Subscription',
                         'description': 'Cool digital posters - Try before subscribing!'})
    token_1 = jwt.encode(jwt_info, SELLER_SECRET)

    # create JWT for second item
    # del request_info['initialPayment']

    initial_payment_info = {'price': '8.00',
                            'currencyCode': 'USD',
                            'paymentType': 'prorated'}
    recurrence_info = {'price': '11.99',
                       'currencyCode': 'USD',
                       'startTime': curr_time + 3*48*3600,
                       'frequency': 'monthly',
                       'numRecurrences': '24'}
    request_info.update({'name': 'Deluxe Posters - Monthly Subscription',
                         'description': 'Subscription to Deluxe Posters',
                         'initialPayment': initial_payment_info,
                         'recurrence': recurrence_info})
    token_2 = jwt.encode(jwt_info, SELLER_SECRET)

    # update store web page
    template_vals = {'jwt_1': token_1,
                     'jwt_2': token_2}

    path = os.path.join(os.path.dirname(__file__), '../templates', 'wallet-demo.html')
    self.response.out.write(template.render(path, template_vals))


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


