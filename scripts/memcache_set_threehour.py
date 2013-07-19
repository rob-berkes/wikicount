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

LANGUAGES=wikilib.getLanguageList()




send_list=[]
THREEHOUR_QUERY=db.threehour.find().sort('place',1)
syslog.syslog('memcache-threehour:  count: '+str(THREEHOUR_QUERY.count()))

for lang in LANGUAGES:
	collNAME=str(lang)+'_threehour'
	keyNAME=str(lang)+'_THREEHOUR'
	THREEHOUR_QUERY=db[collNAME].find().sort('place',1)
	for p in THREEHOUR_QUERY:
		rec={'title':p['title'],'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id']}
		wikilib.GenInfoPage(p['id'],lang)
       	 	send_list.append(rec)
	wikilib.fnSetMemcache('THREEHOUR_LIST_QUERY',send_list,60*60) 


#wikilib.fnLaunchNextJob('set_threehour')


