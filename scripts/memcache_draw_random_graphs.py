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



syslog.syslog('draw_random.py: starting...')
print 'random query...'
send_list=[]
RANDOM_LIST_QUERY=mc.get('RANDOM_ARTICLES')
for a in RANDOM_LIST_QUERY:
        wikilib.GenInfoPage(a['id'])
syslog.syslog('draw_random.py: done!')
wikilib.fnLaunchNextJob('random')
