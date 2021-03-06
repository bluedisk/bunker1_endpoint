# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import time

import webapp2
from models import Weekly
from datetime import date

from push import push_to, push_to_all

from google.appengine.api import memcache

import logging
logging.getLogger().setLevel(logging.INFO)

# get post list - mobile
def getMobileWeeklyList():
    res = requests.get('http://bunker1church.com/')
    soup = BeautifulSoup(res.text)

    regex = re.compile(ur'([0-9]{1,2})[월/]?[ \t]*([0-9]{1,2})일?[ \t]?(.*)$');

    weeklies = [];

    cur_year = int(date.today().year)
    if date.today().month == 12: 
        cur_year = cur_year + 1

    for sermon in soup.find_all(class_='under-slider-sermon-wrapper') + soup.find_all(class_='sermon-content-wrapper'):
        title = sermon.find(class_='sermon-title').find('span')
        if not title:
            title = sermon.find(class_='sermon-title')

        group = regex.match(title.text).groups();
        
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
			result = Weekly.query(Weekly.date == weekly['date']).fetch()

			if not result:
				data = Weekly()
				data.title = weekly['title']
				data.date = weekly['date']
				data.speaker = weekly['speaker']
				data.link = weekly['link']
				data.put()
				updated_count = updated_count + 1


		if updated_count:
			logging.info("Update %d items"%updated_count)

		if updated_count or not memcache.get('weekly'):
			self.update_memcache()

		if updated_count == 1:
			push_to_all(u"새로운 주보가 등록되었습니다. 다운로드 해주세요!",updated_count);
		elif updated_count >= 2:
			push_to_all(u"%s개의 새로운 주보가 등록되었습니다. 다운로드 해주세요!"%updated_count,updated_count);

	def update_memcache(self):
		weeklys = Weekly.query().fetch()

		digested = []
		for weekly in weeklys:
			digested.append({
				'title' : weekly.title,
            	'speaker' : weekly.speaker,
            	'date' : weekly.date.strftime('%Y%m%d'),
            	'link' : weekly.link,
			})


		memcache.set('weekly', digested, 60*60)



app = webapp2.WSGIApplication([('.*', MainHandler) ], debug=True)


