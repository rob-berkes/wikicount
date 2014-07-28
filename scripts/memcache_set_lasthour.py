#!/usr/bin/python
import memcache 
import string 
import urllib2
import random
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




SEARCH_HOUR='%02d' % (int(HOUR),)
print SEARCH_HOUR
HOURQUERY=db.hitshourlydaily.find({str(SEARCH_HOUR):{'$gt':1}}).sort(str(SEARCH_HOUR),-1).limit(50)
send_list=[]
place=1
syslog.syslog('memcache-hourly: '+' count: '+str(HOURQUERY.count()))
for row in HOURQUERY:
    title,utitle=wikilib.fnFindName(row['_id'])
    wikilib.GenInfoPage(row['_id'])
    rec={'place':place,'Hits':row[str(SEARCH_HOUR)],'title':title ,'id':str(row['_id']),'linktitle':title}
    place+=1
    send_list.append(rec)
print len(send_list)
wikilib.fnSetMemcache('HOURKEY',send_list,60*60*3)
wikilib.fnLaunchNextJob('set_lasthour')
