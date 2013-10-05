from pymongo import Connection
from functions import wikilib
from multiprocessing import Process, Pipe
from lib import sorting
import math
import time
import os
BEGINTIME=time.time()
conn=Connection('10.170.44.106')
db=conn.wc
lang='en'
HD=str(lang)+'_hitsdaily'
HH=str(lang)+'_hitshourly'
SD=str(lang)+'_similarity'
DATE1="2013_10_03"


def makeArray(LLIST):
	st=time.time()
        NEWARRAY=[]
        for i in LLIST:
                rec=(i['TOTAL'],i['_id'],i['title'])
                NEWARRAY.append(rec)
	et=time.time()
	tt=et-st
	print('array made in '+str(tt)+' seconds.')
        return NEWARRAY
        
def getDayList():
	HD=str(lang)+'_hitsdaily'
	SD=str(lang)+'_similarity'
	HH=str(lang)+'_hitshourly'
	DATE1="2013_10_03"
        RSET=db[HD].find({DATE1:{'$gt':120}},limit=100000)
        return RSET.limit(100000)
def scoreList(D1Q,H1Q,HRAT1,HRAT2,MATCHLIST):
        STIME=time.time()
        NLIST=[]
	SCOREGOODS=0
	SCOREBADS=0
        for m in MATCHLIST:
		TOTDIFF=0
		HOURRES=db[HH].find_one({'_id':m['_id']})
		try:
			h1RATIO=float(HOURRES['16'])/float(HOURRES['23'])							
			SCOREGOODS+=1
		except:
			SCOREBADS+=1
			continue
		try:
			h2RATIO=float(HOURRES['08'])/float(HOURRES['16'])
			SCOREGOODS+=1
		except:
			SCOREBADS+=1
			continue
		TOTDIFF+=math.fabs(h2RATIO-HRAT2)+math.fabs(h1RATIO-HRAT1)
		for SLMONTH in range(10,11):
			for SLDAY in range(2,5):
				SSLMONTH="%02d" % (SLMONTH,)
				SSLDAY="%02d" % (SLDAY,)
				YSSLDAY="%02d" % (SLDAY-1,)
				STRINGDATE="2013_"+SSLMONTH+"_"+SSLDAY
				YSTRINGDATE="2013_"+SSLMONTH+"_"+YSSLDAY
				try:
					mRATIO=float(m[STRINGDATE])/float(m[YSTRINGDATE])
					D1QRATIO=float(D1Q[STRINGDATE])/float(D1Q[YSTRINGDATE])
					TOTDIFF+=math.fabs(D1QRATIO-mRATIO)
				except ZeroDivisionError:
					continue
				except KeyError:
					continue
                rec={'_id':m['_id'],'title':m['title'],'TOTAL':TOTDIFF}
		if m['_id']!=ID and TOTDIFF!=0:
	                NLIST.append(rec)
        ETIME=time.time()
        TTIME=ETIME-STIME
        print 'scoring done in '+str(TTIME)+' seconds. ScoreGoods: '+str(SCOREGOODS)+' ScoreBads: '+str(SCOREBADS)
        return NLIST


STARTTIME=time.time()
MATCHLIST=getDayList()
ENDTIME=time.time()
TTIME=ENDTIME-STARTTIME
print "found "+ str(MATCHLIST.count())+" records in "+str(TTIME)+" seconds, now scoring..."

COUNT=1
HOUREXCEPTS=0
HOURGOODS=0
ENTHREE=db['en_threehour'].find()
for m in ENTHREE:
	MATCHLIST.rewind()
	print 'record '+str(COUNT)
	COUNT+=1
        ID=m['id']
        TITLE=m['title']
        D1Q=db[HD].find_one({'_id':ID})
	H1Q=db[HH].find_one({'_id':ID})
	try:	
		HRAT1=float(H1Q['16'])/float(H1Q['23'])
		HOURGOODS+=1
	except:
		HOUREXCEPTS+=1
		HRAT1=0
	try:
		HRAT2=float(H1Q['08'])/float(H1Q['16'])
		HOURGOODS+=1
	except:
		HOUREXCEPTS+=1
		HRAT2=0
	print 'HRAT1 '+str(HRAT1)+' HRAT2 '+str(HRAT2)

        NEWLIST=scoreList(D1Q,H1Q,HRAT1,HRAT2,MATCHLIST)
        NEWARRAY=makeArray(NEWLIST)
	
	st=time.time()
        SORTLIST=sorting.QuickSortListArray(NEWARRAY,'asc')
	et=time.time()
	tt=et-st
	print 'list sorted in '+str(tt)+' seconds.'

	LC=1
	db[SD].remove({'_id':ID})
	SDLIST=[]
	for rec in SORTLIST:
	   	if LC>11:
	               	break
		nrec={'id':rec[1],'title':rec[2],'score':str(rec[0])[0:5]}
		SDLIST.append(nrec)
        	LC+=1
	IREC={'_id':str(ID),'similars':SDLIST}
	print IREC
	db[SD].insert(IREC)

ENDTIME=time.time()
print 'all done in '+str(ENDTIME-BEGINTIME)+' seconds!'
