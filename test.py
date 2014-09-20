# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import time

from datetime import date


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

for w in getMobileWeeklyList():
    print w['author'] 
    
