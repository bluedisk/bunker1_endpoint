# -*- coding: utf-8 -*-

import webapp2
from google.appengine.ext import ndb

from settings import connectToAPNS

from models import PushError, Token
from datetime import datetime

import logging
logging.getLogger().setLevel(logging.INFO)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        apns = connectToAPNS()

        for (token_hex, fail_time) in apns.feedback_server.items():

            fail_time = float(fail_time)
            logging.debug("token:%s time:%s"%(token_hex, fail_time))

            ndb.Key(Token,token_hex).delete()

            error = PushError(token_hex = token_hex, deleted_at = datetime.utcfromtimestamp(fail_time))
            error.put()


app = webapp2.WSGIApplication([('.*', MainHandler) ], debug=True)


