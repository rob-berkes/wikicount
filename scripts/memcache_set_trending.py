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
RSET=db.logSystem.find_one({'table':'populate_image'})

send_list=[]    
TRENDING_LIST_QUERY=db.prodtrend.find({u'd':DAY,u'm':MONTH,u'y':YEAR}).sort('Hits',-1).limit(150)
syslog.syslog('memcache-hour-trending: count: '+str(TRENDING_LIST_QUERY.count()))
print TRENDING_LIST_QUERY.count()
COUNTER=0
for p in TRENDING_LIST_QUERY:
	rec={'title':p['title'],'place':p['place'],'Hits':p['Hits'],'linktitle':p['linktitle'],'id':p['id']}
        send_list.append(rec)
	COUNTER+=1
	wikilib.GenInfoPage(p['id'])
syslog.syslog('memcache-hour-trending: '+str(COUNTER)+' pages appended succesfully.')
syslog.syslog('memcache-hour-trending: '+str(len(send_list))+' items in send_list.')
wikilib.fnSetMemcache('HOURKEY',send_list,60*60*3)
wikilib.fnLaunchNextJob('set_trending')


