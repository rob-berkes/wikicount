#!/usr/bin/python
#import redis
import string 
import urllib2
from pymongo import Connection
from datetime import date
from datetime import time
from functions import wikilib
import datetime
import subprocess
import syslog
import os
import redis

conn=Connection('10.37.11.218')
db=conn.wc

LANGUAGES=wikilib.getLanguageList()

Cli=redis.Redis('10.244.138.64')


send_list=[]
syslog.syslog("3hr: Starting threehour.py with "+str(len(LANGUAGES))+" languages.")
for lang in LANGUAGES:
	collNAME=str(lang)+'_threehour'
	THREEHOUR_QUERY=db[collNAME].find().sort('place',1)
	PLACEMENT=0
	for p in THREEHOUR_QUERY:
		PLACEMENT+=1
		tstr=str(p['title'])
		REDIS_TITLE_KEY=str(lang)+'_'+str(p['id'])+'_TITLE'
		REDIS_AVG_KEY=str(lang)+'_'+str(p['id'])+'_'+'AVG'
		REDIS_LINKTITLE_KEY=str(lang)+'_'+str(p['id'])+'_'+'LINKTITLE'
		REDIS_ID_KEY=str(lang)+'_'+str(PLACEMENT)+'_'+'ID'
		#wikilib.GenInfoPage(p['id'],lang)
     	 	Cli.set(REDIS_TITLE_KEY,urllib2.unquote(tstr))
		Cli.set(REDIS_AVG_KEY,p['rollavg'])
		Cli.set(REDIS_LINKTITLE_KEY,p['title'])
		Cli.set(REDIS_ID_KEY,p['id'])
	syslog.syslog('3hr: Finished '+str(lang)+' at '+str(PLACEMENT)+' , onto next language.')

syslog.syslog('3hr: finished altogether with threehour.py')




