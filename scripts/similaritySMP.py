from pymongo import Connection
from itertools import izip
from lib import wikilib
from multiprocessing import Process, Pipe,Queue
from lib import sorting
import math
import time
import os
BEGINTIME=time.time()
conn=Connection(wikilib.MONGO_IP)
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
def dayScore(cconn):
	D1Q=cconn.recv()
	HRAT1=cconn.recv()
	HRAT2=cconn.recv()
	m=cconn.recv()
	print 'dayScore entry '
	print D1Q
	print m
	SCOREGOODS=0
	SCOREBADS=0
	TOTDIFF=0
	for SLMONTH in range(10,11):
		for SLDAY in range(2,5):
			SSLMONTH="%02d" % (SLMONTH,)
			SSLDAY="%02d" % (SLDAY,)
			YSSLDAY="%02d" % (SLDAY-1,)
			STRINGDATE="2013_"+SSLMONTH+"_"+SSLDAY
			print STRINGDATE
			YSTRINGDATE="2013_"+SSLMONTH+"_"+YSSLDAY
			try:
				mRATIO=float(m[STRINGDATE])/float(m[YSTRINGDATE])
				D1QRATIO=float(D1Q[STRINGDATE])/float(D1Q[YSTRINGDATE])
				TOTDIFF+=math.fabs(D1QRATIO-mRATIO)
			except ZeroDivisionError:
				print 'zde error!'
			except KeyError:
				TOTDIFF+=1
	print ' doing hours'
	HOURRES=db[HH].find_one({'_id':m['_id']})
	try:
		h1RATIO=float(HOURRES['16'])/float(HOURRES['23'])							
		SCOREGOODS+=1
	except:
		SCOREBADS+=1
		h1RATIO=1
	try:
		h2RATIO=float(HOURRES['08'])/float(HOURRES['16'])
		SCOREGOODS+=1
	except:
		SCOREBADS+=1
		h2RATIO=1
	TOTDIFF+=math.fabs(h2RATIO-HRAT2)+math.fabs(h1RATIO-HRAT1)
	rec={'_id':m['_id'],'title':m['title'],'TOTAL':TOTDIFF}
	print 'sending rec'
	print rec
	cconn.send(rec)

def threewise(LLIST):
	a=iter(LLIST)
	return izip(a,a,a)

def scoreList(MATCHLIST,p,q,r,p1,q1,r1):
        STIME=time.time()
        NLIST=[]
	SCOREGOODS=0
	SCOREBADS=0
        for m,mN,mO in threewise(MATCHLIST):
		print 'm'
		p1.send(m)
		q1.send(mN)
		print 'mN='
		r1.send(mO)
		print 'mO'

		id1=p1.recv()
		print 'id1'
		print id1
		id2=q1.recv()
		print 'id2'
		print id2
		id3=r1.recv()
		print 'id3'
		print id3
		
	        NLIST.append(id1)
		print 'id1 appended!'
		NLIST.append(id2)
		print 'id2 appended'
		NLIST.append(id3)
		print 'id3 appended!'
        ETIME=time.time()
        TTIME=ETIME-STIME
        print 'scoring done in '+str(TTIME)+' seconds. NList size: ' +str(len(NLIST))
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
p1,pc1=Pipe()
q1,qc1=Pipe()
r1,rc1=Pipe()
p=Process(target=dayScore,args=(pc1,))
q=Process(target=dayScore,args=(qc1,))
r=Process(target=dayScore,args=(rc1,))
p.start()
q.start()
r.start()	
for m in ENTHREE:
	MATCHLIST.rewind()
	print 'record '+str(COUNT)
	COUNT+=1
        ID=m['id']
	D1Q=db[HD].find_one({'_id':ID})
        TITLE=m['title']
	p1.send(D1Q)
	q1.send(D1Q)
	r1.send(D1Q)
	H1Q=db[HH].find_one({'_id':ID})
	try:	
		HRAT1=float(H1Q['16'])/float(H1Q['23'])
		HOURGOODS+=1
	except:
		HOUREXCEPTS+=1
		HRAT1=1
	p1.send(HRAT1)
	q1.send(HRAT1)
	r1.send(HRAT1)

	try:
		HRAT2=float(H1Q['08'])/float(H1Q['16'])
		HOURGOODS+=1
	except:
		HOUREXCEPTS+=1
		HRAT2=1
	p1.send(HRAT2)
	q1.send(HRAT2)
	r1.send(HRAT2)

	print 'HRAT1 '+str(HRAT1)+' HRAT2 '+str(HRAT2)
        NEWLIST=scoreList(MATCHLIST,p,q,r,p1,q1,r1)
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

p.terminate()
q.terminate()
r.terminate()
ENDTIME=time.time()
print 'all done in '+str(ENDTIME-BEGINTIME)+' seconds!'
