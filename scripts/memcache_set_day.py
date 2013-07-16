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
DAILYPAGERESULTS=db.command({'distinct':thCN,'key':'d','query':{'m':int(MONTH)}})



HOUR=datetime.datetime.now().strftime('%H')
HOUR=wikilib.fnMinusHour(int(HOUR))
RSET=db.logSystem.find_one({'table':'populate_image'})

send_list=[]
syslog.syslog('calling daily pages image script....')
for d in DAILYPAGERESULTS['values']:
	rec={'d':d,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(d)}
        send_list.append(rec)
wikilib.fnSetMemcache('mcdpDaysList'+str(MONTH)+str(YEAR),send_list,60*60*24)



QUERY={'d':DAY,'m':MONTH,'y':YEAR}
send_list=[]
RESULTSET=db[thCN].find(QUERY).sort('place',1).limit(100)
syslog.syslog('memcache-daily: '+str(QUERY)+' count: '+str(RESULTSET.count()))
for row in RESULTSET:
	wikilib.GenInfoPage(row['id'])
	title,utitle=wikilib.fnFormatName(row['title'])
        rec={'place':row['place'],'Hits':row['Hits'],'title':utitle ,'id':str(row['id']),'linktitle':title.encode('utf-8')}
        send_list.append(rec)
wikilib.fnSetMemcache('DAYKEY',send_list,7200)
notedate=''
notes=''
latest_hits_list = db[thCN].find(QUERY).sort('place',1).limit(100)
syslog.syslog('memcache-latest: '+str(QUERY)+' count: '+str(latest_hits_list.count()))
for p in latest_hits_list:
	wikilib.GenInfoPage(p['id'])
        title,utitle=wikilib.fnFormatName(p['title'])
	rec={'title':utitle,'place':p['place'],'Hits':p['Hits'],'linktitle':title.encode('utf-8'),'notedate':notedate,'notes':notes,'id':p['id']}
        send_list.append(rec)
wikilib.fnSetMemcache('send_list',send_list,3600)

wikilib.fnLaunchNextJob('set_day')
