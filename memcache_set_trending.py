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
DAILYPAGERESULTS=db.command({'distinct':thCN,'key':'d','query':{'m':int(MONTH)}})



HOUR=datetime.datetime.now().strftime('%H')
HOUR=wikilib.fnMinusHour(int(HOUR))
RSET=db.logSystem.find_one({'table':'populate_image'})

send_list=[]    
TRENDING_LIST_QUERY=db.prodtrend.find({u'd':DAY,u'm':MONTH,u'y':YEAR}).sort('Hits',-1).limit(150)
syslog.syslog('memcache-trending: count: '+str(TRENDING_LIST_QUERY.count()))
print TRENDING_LIST_QUERY.count()
for p in TRENDING_LIST_QUERY:
	rec={'title':p['title'],'place':p['place'],'Hits':p['Hits']%1000,'linktitle':p['linktitle'],'id':p['id']}
        send_list.append(rec)
	wikilib.GenInfoPage(p['id'])
wikilib.fnSetMemcache('TRENDING_LIST_QUERY',send_list,1800)



