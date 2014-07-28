#!/usr/bin/python
import memcache 
import string 
from pymongo import Connection
from datetime import date
from datetime import time
from lib import wikilib
import datetime
import subprocess
import syslog
import os

conn=Connection('10.164.95.114')
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

print 'debuts query...'
send_list=[]
title=''
utitle=''
QUERY=db[dbCN].find({u'd':DAY,u'm':MONTH,u'y':YEAR}).sort('place',1).limit(100)
syslog.syslog('memcache-debuts: count: '+str(QUERY.count()))
for item in QUERY:
	COUNT=0
        TITLE=''
	wikilib.GenInfoPage(item['id'])
	title,utitle=wikilib.fnFormatName(item['title'])

	rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':item['linktitle'],'id':item['id']}
        send_list.append(rec)
wikilib.fnSetMemcache('DEBUTS_ARTICLES',send_list,60*60)
wikilib.fnLaunchNextJob('set_debuts')
