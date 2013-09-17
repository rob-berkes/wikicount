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

conn=Connection('10.170.43.109')
db=conn.wc

LANGUAGES=wikilib.getLanguageList()

#Cli=redis.Redis('localhost')


send_list=[]
syslog.syslog("3hr: Starting threehour.py with "+str(len(LANGUAGES))+" languages.")
for lang in LANGUAGES:
	collNAME=str(lang)+'_threehour'
	keyNAME=str(lang)+'_THREEHOUR'
	THREEHOUR_QUERY=db[collNAME].find().sort('place',1)
	PLACEMENT=0
	for p in THREEHOUR_QUERY:
		PLACEMENT+=1
		tstr=str(p['title'])
#		REDIS_TITLE_KEY=str(lang)+'_'+str(PLACEMENT)+'_'+'TITLE'
#		REDIS_PLACE_KEY=str(lang)+'_'+str(PLACEMENT)+'_'+'PLACE'
#		REDIS_AVG_KEY=str(lang)+'_'+str(PLACEMENT)+'_'+'AVG'
#		REDIS_LINKTITLE_KEY=str(lang)+'_'+str(PLACEMENT)+'_'+'LINKTITLE'
#		REDIS_ID_KEY=str(lang)+'_'+str(PLACEMENT)+'_'+'ID'
#		REDIS_LANG_KEY=str(lang)+'_'+str(PLACEMENT)+'_'+'LANG'
		rec={'title':urllib2.unquote(tstr),'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id'],'LANG':str(lang)}
		wikilib.GenInfoPage(p['id'],lang)
 #     	 	Cli.rpush(REDIS_TITLE_KEY,urllib2.unquote(tstr))
#		Cli.rpush(REDIS_PLACE_KEY,p['place'])
#		Cli.rpush(REDIS_AVG_KEY,p['rollavg'])
#		Cli.rpush(REDIS_LINKTITLE_KEY,p['title'])
#		Cli.rpush(REDIS_ID_KEY,p['id'])
	syslog.syslog('3hr: Finished '+str(lang)+' , onto next language.')

syslog.syslog('3hr: finished altogether with threehour.py')




