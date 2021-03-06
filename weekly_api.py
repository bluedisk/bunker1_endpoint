# -*- coding: utf-8 -*-

"""Bunker 1 Church Weekly API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""
import urllib
import endpoints
from google.appengine.api import memcache

from protorpc import messages
from protorpc import message_types
from protorpc import remote

from models import Weekly, Token

from push import push_to, push_to_all

from datetime import datetime

package = 'Weekly'

class WeeklyMessage(messages.Message):
  """Weekly that stores a message."""
  title = messages.StringField(1)
  speaker = messages.StringField(2)
  date = messages.StringField(3)
  link = messages.StringField(4)


class WeeklyCollection(messages.Message):
  """Collection of Weeklies."""
  items = messages.MessageField(WeeklyMessage, 1, repeated=True)
  store = messages.StringField(2)

class RegistTokenResult(messages.Message):
  result = messages.StringField(1)

def getWeeklyList():
  store = 'mem'
  data = memcache.get('weekly')

  if not data:
    store = 'db'
    data = [{
      'title' : weekly.title,
      'speaker' : weekly.speaker,
      'date' : weekly.date.strftime('%Y%m%d'),
      'link' : weekly.link,
    } for weekly in Weekly.query().fetch()]

  return (data, store)

@endpoints.api(name='bunker1cc', version='v1')
class B1CWeeklyApi(remote.Service):
    """Bunker 1 Church Weekly API v1."""

    @endpoints.method(message_types.VoidMessage, WeeklyCollection,
                      path='weekly', http_method='GET',
                      name='weekly.list')
    def weeklies_list(self, unused_request):
      data, store = getWeeklyList()

      weeklies = WeeklyCollection(items = [WeeklyMessage(**weekly) for weekly in data ], store=store)

      return weeklies

    WHEN_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            when=messages.StringField(1))

    @endpoints.method(WHEN_RESOURCE, WeeklyMessage,
                      path='weekly/{when}', http_method='GET',
                      name='weekly.get')
    def weeklies_get(self, request):
        when = datetime.strptime(request.when,'%Y%m%d')
        data = Weekly.query(Weekly.date==when).fetch(1)

        if len(data) != 1 :
            raise endpoints.NotFoundException('Weekly %s not found.' % (request.id,))

        weekly = data[0]

        return WeeklyMessage(
            title = weekly['title'],
            speaker = weekly['speaker'],
            date = weekly['date'],
            link = weekly['link'],
            )

    REG_RESOURCE = endpoints.ResourceContainer(
              message_types.VoidMessage,
              token=messages.StringField(2),
              )

    @endpoints.method(REG_RESOURCE, RegistTokenResult,
                      path='regist/{token}', http_method='POST',
                      name='weekly.regist')
    def regist_token(self, request):
        if Token.query(Token.token==request.token).fetch():
          return RegistTokenResult(result="DUP")

        token = Token(token=request.token, os='ios');
        token.put();

        push_to(token, u"환영합니다! 벙커원 교회 주보 알림목록에 등록되었습니다!", 0)

        return RegistTokenResult(result="OK")


@endpoints.api(name='bunker1cc', version='v2')
class B1CWeeklyApiV2(remote.Service):
    """Bunker 1 Church Weekly API v2."""

    @endpoints.method(message_types.VoidMessage, WeeklyCollection,
                      path='weekly', http_method='GET',
                      name='weekly.list')
    def weeklies_list(self, unused_request):
      data, store = getWeeklyList()

      weeklies = WeeklyCollection(items = [WeeklyMessage(**weekly) for weekly in data ], store=store)

      return weeklies


    WHEN_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            when=messages.StringField(1))

    @endpoints.method(WHEN_RESOURCE, WeeklyMessage,
                      path='weekly/{when}', http_method='GET',
                      name='weekly.get')
    def weeklies_get(self, request):
        when = datetime.strptime(request.when,'%Y%m%d')
        data = Weekly.query(Weekly.date==when).fetch(1)

        if len(data) != 1 :
            raise endpoints.NotFoundException('Weekly %s not found.' % (request.id,))

        weekly = data[0]

        return WeeklyMessage(
            title = weekly['title'],
            speaker = weekly['speaker'],
            date = weekly['date'],
            link = weekly['link'],
            )

    REG_RESOURCE = endpoints.ResourceContainer(
              message_types.VoidMessage,
              token=messages.StringField(2),
              os=messages.StringField(3),
              width=messages.StringField(4),
              height=messages.StringField(5)
              )

    @endpoints.method(REG_RESOURCE, RegistTokenResult,
                      path='regist/{token}/{os}/{width}/{height}', http_method='POST',
                      name='weekly.regist')
    def regist_token(self, request):
        if Token.query(Token.token==request.token).fetch():
          return RegistTokenResult(result="DUP")

        token = urllib.unquote(request.token)
        token = Token(token=request.token, os=request.os, width=request.width, height=request.height);
        token.put();

        push_to(token, u"환영합니다! 벙커원 교회 주보 알림목록에 등록되었습니다!", 0)

        return RegistTokenResult(result="OK")


APPLICATION = endpoints.api_server([B1CWeeklyApi,B1CWeeklyApiV2])


