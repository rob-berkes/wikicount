#!/usr/bin/python
import memcache 
import string 
import urllib2
import random
from pymongo import Connection
from datetime import date
from datetime import time
from functions import wikilib
import datetime
import subprocess
import syslog
import os

conn=Connection('10.115.126.7')
db=conn.wc
mc=memcache.Client(['127.0.0.1:11211'],debug=0)
TODAY=date.today()
DAY=TODAY.day
MONTH=TODAY.month
YEAR=TODAY.year
HOUR=wikilib.fnGetHour()

MONTHNAME=datetime.datetime.now().strftime("%B")
thCN='tophits'+str(YEAR)+MONTHNAME
dbCN='proddebuts'+str(YEAR)+str(MONTHNAME)



HOUR=datetime.datetime.now().strftime('%H')
HOUR=wikilib.fnMinusHour(int(HOUR))
RSET=db.logSystem.find_one({'table':'populate_image'})




print 'random query...'
send_list=[]
for a in range(1,50):
	place=random.randint(1,250000)
        FQUERY={u'd':DAY,u'm':MONTH,u'y':YEAR,'place':place}
        RANDOM_LIST_QUERY=db[thCN].find(FQUERY)
        for item in RANDOM_LIST_QUERY:
        	 id=item['id']
		 wikilib.GenInfoPage(item['id'])
       		 title,utitle=wikilib.fnFormatName(item['title']) 
        	 rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':title.encode('utf-8'),'id':item['id']}
        	 send_list.append(rec)
wikilib.fnSetMemcache('RANDOM_ARTICLES',send_list,60*60)


