#!/usr/bin/python
#import redis
import string 
import urllib2
from pymongo import Connection
from datetime import date
from datetime import time
from functions import wikilib
from multiprocessing import Process 
import datetime
import subprocess
import syslog
import os

conn=Connection('10.170.44.106')
db=conn.wc
def splitLanguageList():
	LANGUAGES=wikilib.getLanguageList()
	L1=[]
	L2=[]
	L3=[]
	L4=[]
	COUNTER=1
	for lang in LANGUAGES:
		if COUNTER==1:
			L1.append(lang)
			COUNTER+=1
		elif COUNTER==2:
			L2.append(lang)
			COUNTER+=1
		elif COUNTER==3:
			L3.append(lang)
			COUNTER+=1
		elif COUNTER==4:
			L4.append(lang)
			COUNTER=1
	return L1,L2,L3,L4

def fnPlotGraphs(LANGUAGES):
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
			rec={'title':urllib2.unquote(tstr),'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id'],'LANG':str(lang)}
			wikilib.GenInfoPage(p['id'],lang)
		syslog.syslog('smp_gnuplot: Finished '+str(PLACEMENT)+' records for '+str(lang)+' , onto next language.')

	return



L1,L2,L3,L4 = splitLanguageList()

a=Process(target=fnPlotGraphs, args=(L1,))
b=Process(target=fnPlotGraphs, args=(L2,))
c=Process(target=fnPlotGraphs, args=(L3,))
d=Process(target=fnPlotGraphs, args=(L4,))

a.daemon=True
b.daemon=True
c.daemon=True
d.daemon=True

a.start()
b.start()
c.start()
d.start()

a.join()
b.join()
c.join()
d.join()





