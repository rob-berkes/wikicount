#!/usr/bin/python
import memcache 
from pymongo import Connection
from datetime import date
from datetime import time
from lib import wikilib
import datetime
import syslog

conn=Connection('10.164.95.114')
db=conn.wc
mc=memcache.Client(['127.0.0.1:11211'],debug=0)
HOUR=wikilib.fnGetHour()
DAY,MONTH,YEAR=wikilib.fnGetDate()
MONTHNAME=wikilib.fnGetMonthName()
thCN='tophits'+str(YEAR)+MONTHNAME
dbCN='proddebuts'+str(YEAR)+str(MONTHNAME)

HOUR=wikilib.fnMinusHour(int(HOUR))
wikilib.fnOpenSitemap()
syslog.syslog('starting memcache_set_cold query')
send_list=[]    
COLD_LIST_QUERY=db.prodcold.find().sort('Hits',1).limit(100)
syslog.syslog('memcache-cold: COLD_LIST_QUERY count: '+str(COLD_LIST_QUERY.count()))
print COLD_LIST_QUERY.count()
a=0
for p in COLD_LIST_QUERY:
	a+=1
	rec={'title':p['title'],'place':p['place'],'Hits':p['Hits'],'linktitle':p['linktitle'],'id':p['id']}
        send_list.append(rec)
	wikilib.GenInfoPage(p['id'])
syslog.syslog('memcache-cold: total of '+str(a)+' records processed')
wikilib.fnSetMemcache('COLD_LIST_QUERY',send_list,60*60*2)
syslog.syslog('memcache-cold: done!')
wikilib.fnLaunchNextJob('set_cold')

