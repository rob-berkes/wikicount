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

#conn=Connection('10.245.145.84')
conn=Connection('10.115.126.7')
db=conn.wc
mc=memcache.Client(['127.0.0.1:11211'],debug=0)
TODAY=date.today()
DAY=TODAY.day
MONTH=TODAY.month
YEAR=TODAY.year
MONTHNAME=datetime.datetime.now().strftime("%B")
thCN='tophits'+str(YEAR)+MONTHNAME
dbCN='proddebuts'+str(YEAR)+str(MONTHNAME)
DAILYPAGERESULTS=db.command({'distinct':thCN,'key':'d','query':{'m':int(MONTH)}})



COLD_LIST_QUERY=mc.get('COLD_LIST_QUERY')
syslog.syslog('memcache-cold:count: '+str(len(COLD_LIST_QUERY)))
print len(COLD_LIST_QUERY)
for p in COLD_LIST_QUERY:
	print p
	wikilib.GenInfoPage(p['id'])

syslog.syslog('memcache-cold: done!')
wikilib.fnLaunchNextJob('cold')
