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

conn=Connection('10.37.11.218')
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





print 'lastly, 3hr rolling average'
send_list=[]
THREEHOUR_QUERY=db.threehour.find().sort('place',1)
syslog.syslog('memcache-threehour:  count: '+str(THREEHOUR_QUERY.count()))

for p in THREEHOUR_QUERY:
	rec={'title':p['title'],'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id']}
	wikilib.GenInfoPage(p['id'])
        send_list.append(rec)
wikilib.fnSetMemcache('THREEHOUR_LIST_QUERY',send_list,60*60) 



