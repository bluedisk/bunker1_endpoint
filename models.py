# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


class Weekly(ndb.Model):
  """Models an individual Guestbook entry with content and date."""
  title = ndb.StringProperty()
  speaker = ndb.StringProperty()
  date = ndb.DateProperty()
  link = ndb.StringProperty()

  updated_at = ndb.DateTimeProperty(auto_now_add=True)

class Token(ndb.Model):
  os = ndb.StringProperty(default='ios')
  
  width = ndb.StringProperty(default='')
  height = ndb.StringProperty(default='')

  token = ndb.StringProperty()
  created_at = ndb.DateTimeProperty(auto_now_add=True)

class PushError(ndb.Model):
  token = ndb.StringProperty()
  deleted_at = ndb.DateTimeProperty()
