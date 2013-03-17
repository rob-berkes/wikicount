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
if int(HOUR) < 4:
	if DAY > 1:
		DAY-=1

MONTHNAME=datetime.datetime.now().strftime("%B")
thCN='tophits'+str(YEAR)+MONTHNAME
dbCN='proddebuts'+str(YEAR)+str(MONTHNAME)
DAILYPAGERESULTS=db.command({'distinct':thCN,'key':'d','query':{'m':int(MONTH)}})



HOUR=datetime.datetime.now().strftime('%H')
HOUR=wikilib.fnMinusHour(int(HOUR))
RSET=db.logSystem.find_one({'table':'populate_image'})

send_list=[]
print 'daily pages first....'
for d in DAILYPAGERESULTS['values']:
	rec={'d':d,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(d)}
        send_list.append(rec)
mc.set('mcdpDaysList',send_list,60*60*24)



QUERY={'d':DAY,'m':MONTH,'y':YEAR}
send_list=[]
RESULTSET=db[thCN].find(QUERY).sort('place',1).limit(100)
syslog.syslog('memcache-daily: '+str(QUERY)+' count: '+str(RESULTSET.count()))
for row in RESULTSET:
	wikilib.GenInfoPage(row['id'])
	title,utitle=wikilib.fnFormatName(row['title'])
        rec={'place':row['place'],'Hits':row['Hits'],'title':utitle ,'id':str(row['id']),'linktitle':title.encode('utf-8')}
        send_list.append(rec)
mc.set('DAYKEY',send_list,7200)
notedate=''
notes=''
latest_hits_list = db[thCN].find(QUERY).sort('place',1).limit(100)
syslog.syslog('memcache-latest: '+str(QUERY)+' count: '+str(latest_hits_list.count()))
for p in latest_hits_list:
	wikilib.GenInfoPage(p['id'])
        title,utitle=wikilib.fnFormatName(p['title'])
	rec={'title':utitle,'place':p['place'],'Hits':p['Hits']%1000,'linktitle':title.encode('utf-8'),'notedate':notedate,'notes':notes,'id':p['id']}
        send_list.append(rec)
mc.set('send_list',send_list,3600)


send_list=[]    
TRENDING_LIST_QUERY=db.prodtrend.find({u'd':DAY,u'm':MONTH,u'y':YEAR}).sort('Hits',-1).limit(150)
syslog.syslog('memcache-trending: '+str(QUERY)+' count: '+str(TRENDING_LIST_QUERY.count()))
print TRENDING_LIST_QUERY.count()
for p in TRENDING_LIST_QUERY:
	rec={'title':p['title'],'place':p['place'],'Hits':p['Hits']%1000,'linktitle':p['linktitle'],'id':p['id']}
        send_list.append(rec)
	wikilib.GenInfoPage(p['id'])
mc.set('TRENDING_LIST_QUERY',send_list,1800)

print 'cold list query'
send_list=[]    
COLD_LIST_QUERY=db.prodcold.find().sort('Hits',1).limit(100)
syslog.syslog('memcache-cold: '+str(QUERY)+' count: '+str(COLD_LIST_QUERY.count()))
print COLD_LIST_QUERY.count()
for p in COLD_LIST_QUERY:
	rec={'title':p['title'],'place':p['place'],'Hits':p['Hits']%1000,'linktitle':p['linktitle'],'id':p['id']}
        send_list.append(rec)
	wikilib.GenInfoPage(p['id'])
mc.set('COLD_LIST_QUERY',send_list,1800)


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
mc.set('RANDOM_ARTICLES',send_list,60*60)



print 'debuts query...'
send_list=[]
title=''
utitle=''
QUERY=db[dbCN].find({u'd':DAY,u'm':MONTH,u'y':YEAR}).sort('place',1).limit(300)
syslog.syslog('memcache-debuts: count: '+str(QUERY.count()))
for item in QUERY:
	COUNT=0
        TITLE=''
	wikilib.GenInfoPage(item['id'])
	title,utitle=wikilib.fnFormatName(item['title'])

	rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':item['linktitle'],'id':item['id']}
        send_list.append(rec)
mc.set('DEBUTS_ARTICLES',send_list,60*60)


print 'lastly, 3hr rolling average'
send_list=[]
THREEHOUR_QUERY=db.threehour.find().sort('place',1)
syslog.syslog('memcache-threehour:  count: '+str(THREEHOUR_QUERY.count()))

for p in THREEHOUR_QUERY:
	rec={'title':p['title'],'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id']}
	wikilib.GenInfoPage(p['id'])
        send_list.append(rec)
mc.set('THREEHOUR_LIST_QUERY',send_list,60*60) 



SEARCH_HOUR='%02d' % (int(HOUR),)
HOURQUERY=db.hitshourlydaily.find({str(SEARCH_HOUR):{'$gt':1}}).sort(str(SEARCH_HOUR),-1).limit(50)
send_list=[]
place=1
HOURKEY="SEARCHHOUR_"+str(SEARCH_HOUR)
syslog.syslog('memcache-hourly: '+' count: '+str(HOURQUERY.count()))
for row in HOURQUERY:
    title,utitle=wikilib.fnFindName(row['_id'])
    wikilib.GenInfoPage(row['_id'])
    rec={'place':place,'Hits':row[str(SEARCH_HOUR)],'title':utitle ,'id':str(row['_id']),'linktitle':title.encode('utf-8')}
    place+=1
    send_list.append(rec)
mc.set(HOURKEY,send_list,30*60)

wikilib.fnLaunchNextJob('set_vars')
