# -*- coding: utf-8 -*-

import webapp2
from google.appengine.ext import ndb

from settings import apns
from apns import APNs
from models import PushError, Token
from datetime import datetime

class MainHandler(webapp2.RequestHandler):
	def get(self):		
		for (token_hex, fail_time) in apns.feedback_server.items():
			
			ndb.Key(Token,token_hex).delete()

			error = PushError(token_hex = token_hex, deleted_at = datetime.utcfromtimestamp(fail_time))
			error.put()


app = webapp2.WSGIApplication([('.*', MainHandler) ], debug=True)


