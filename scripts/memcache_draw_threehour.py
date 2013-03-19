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
MONTHNAME=datetime.datetime.now().strftime("%B")
thCN='tophits'+str(YEAR)+MONTHNAME
dbCN='proddebuts'+str(YEAR)+str(MONTHNAME)
DAILYPAGERESULTS=db.command({'distinct':thCN,'key':'d','query':{'m':int(MONTH)}})

THREEHOUR_QUERY=mc.get('THREEHOUR_LIST_QUERY')
send_list=[]
syslog.syslog('draw-threehour:  starting....')
for p in THREEHOUR_QUERY:
	print p['title']
	rec={'title':p['title'],'place':p['place'],'Avg':p['Avg'],'linktitle':p['title'],'id':p['id']}
	wikilib.GenInfoPage(p['id'])
        send_list.append(rec)
syslog.syslog('draw-threehour: done!')
mc.set('THREEHOUR_LIST_QUERY',send_list,60*60) 

wikilib.fnLaunchNextJob('threehour')
