# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re

import webapp2
from models import Weekly, Token
from datetime import date

import time
from apns import APNs, Frame, Payload

import logging
logging.getLogger().setLevel(logging.DEBUG)

# get post list - mobile
def getMobileWeeklyList():
	res = requests.get('http://bunker1church.com/')
	soup = BeautifulSoup(res.text)

	regex = re.compile(ur'([0-9]{1,2})[월/]?[ \t]*([0-9]{1,2})일?[ \t](.*)$');

	weeklies = [];

	cur_year = int(date.today().year)
	if date.today().month == 12: 
		cur_year = cur_year + 1

	for sermon in soup.find_all(class_='sermon-content-wrapper'):
		group = regex.match(sermon.find(class_='sermon-title').find('span').text).groups();
		
		title = group[2]
		cur_month = int(group[0])
		cur_day = int(group[1])

		if cur_month  == 12:
			cur_year = cur_year - 1

		weekly = {
			"title":title,
			"date":date(cur_year, cur_month, cur_day),
			"speaker":re.search(u":[ \t]*(.*)",unicode(sermon.find(class_='sermon-author').text)).group(1),
			"link":sermon.find(class_='sermon-pdf').find('a')['href']
		}

		weeklies.append(weekly)



	return weeklies


# get post list - daum
# res = requests.get('http://cluster1.cafe.daum.net/_c21_/bbs_list?grpid=1Q8gm&fldid=8eVX')
# soup = BeautifulSoup(res.text)

# for sermon in soup.find(class_='bbsList').find_all('tr'):
# 	subject = sermon.find(class_='subject')
# 	num = sermon.find(class_='num')

# 	if subject and num and num.text:
# 		print subject.find('a').text
# 		print "http://cafe.daum.net/bunker1church/8eVX/"+num.text


# get file url from daum post
# res = requests.get('http://cafe.daum.net/bunker1church/8eVX/99')
# soup = BeautifulSoup(res.text)

# href = soup.find(id='down')['src']

# res = requests.get(href)
# soup = BeautifulSoup(res.text)
# content = soup.find('xmp').text

# soup = BeautifulSoup(content)

# href = soup.find('a')['href']
# mat = re.search(r'url=(.*)"',href)

# fileurl = urllib.unquote(mat.group(1))


class MainHandler(webapp2.RequestHandler):
	def get(self):
		weeklies = getMobileWeeklyList()
		updated_count = 0


		for weekly in weeklies:
			result = Weekly.query(Weekly.title == weekly['title']).fetch()

			if not result:
				data = Weekly()
				data.title = weekly['title']
				data.date = weekly['date']
				data.speaker = weekly['speaker']
				data.link = weekly['link']
				data.put()
				updated_count = updated_count + 1


		logging.debug("Update %d items"%updated_count)

		if updated_count == 1:
			send_to_all(u"새로운 주보가 등록되었습니다. 다운로드 해주세요!",updated_count);
		elif updated_count >= 2:
			send_to_all(u"%s개의 새로운 주보가 등록되었습니다. 다운로드 해주세요!"%updated_count,updated_count);



def send_to_all(text, count):
	apns = APNs(use_sandbox=True, cert_file='certs/bunker1cc_apns_dist.pem', key_file='certs/bunker1cc_apns_dist.pem')

	payload = Payload(alert=text, sound="default", badge=count)
	tokens = Token.query().fetch()

	for token in tokens:
		apns.gateway_server.send(token.token, payload)

	logging.debug("send to push : total %d tokens"%len(tokens))


app = webapp2.WSGIApplication([('.*', MainHandler) ], debug=True)


