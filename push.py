# -*- coding: utf-8 -*-
import webapp2

from settings import connectToAPNS, connectToGCM
from apns import APNs,Payload
from models import Token

apns_conn = None
gcm_conn = None

def push_to(token, text, count):
    if token.os == 'android':
        push_to_gcm(token.token, text, count)
    else:
        push_to_apns(token.token, text, count)

def push_to_gcm(keys, text, count):
    global gcm_conn
    if not gcm_conn:
        gcm_conn = connectToGCM()
    gcm_conn.send(keys,text)

def push_to_apns(key, text, count):
    global apns_conn
    if not apns_conn:
        apns_conn = connectToAPNS()

    payload = Payload(alert=text, sound="default", badge=count)

    apns = connectToAPNS();
    apns.gateway_server.send(key, payload)

    
def push_to_all(text, count):

    ios_tokens = Token.query(Token.os!='android').fetch()
    and_tokens = Token.query(Token.os=='android').fetch()

    for token in ios_tokens:
        push_to_apns(token.token, text, count)

    push_to_gcm(list(token.token for token in and_tokens), text, count)

    #logging.debug("send to push : total %d tokens"%(len(ios_tokens)+len(and_tokens)))



class MainHandler(webapp2.RequestHandler):
    def get(self):

        and_tokens = Token.query(Token.os=='android').fetch()
        push_to_gcm(list(token.token for token in and_tokens), 'push test', 1)


app = webapp2.WSGIApplication([('.*', MainHandler) ], debug=True)
