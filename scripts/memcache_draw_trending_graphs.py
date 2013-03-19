#!/usr/bin/python
import memcache 
import string 
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




syslog.syslog('draw_trending.py: starting....')
send_list=[]    
TRENDING_QUERY=mc.get('TRENDING_LIST_QUERY')
for p in TRENDING_QUERY:
	rec={'title':p['title'],'place':p['place'],'Hits':p['Hits'],'linktitle':p['linktitle'],'id':p['id']}
        send_list.append(rec)
	wikilib.GenInfoPage(p['id'])
syslog.syslog('draw_trending.py: done!')
wikilib.fnLaunchNextJob('trending')
