from pymongo import Connection
from functions import wikilib
from multiprocessing import Process, Pipe
from lib import sorting
import math
import time
import os

#ID='d0f26dab5386f3b1bfd8d4387bf1b15ad423de92'
conn=Connection('10.170.44.106')
db=conn.wc
lang='en'
HD=str(lang)+'_hitsdaily'
SD=str(lang)+'_similarity'
DATE1="2013_09_30"
DATE2="2013_09_28"
DATE3="2013_09_22"
DATE4="2013_09_21"
DATE5="2013_10_01"


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
        RSET=db[HD].find({DATE1:{'$gt':75}})
	RLIST=[]
        for r in RSET:
                try:
                        rec={'_id':r['_id'],'title':r['title'],DATE1:r[DATE1],DATE2:r[DATE2],DATE3:r[DATE3],DATE4:r[DATE4]}
                        #rec={'_id':r['_id'],DATE1:r[DATE1],DATE2:r[DATE2]}
                        RLIST.append(rec)
                except NameError:
                        pass
                except KeyError:
                        pass
        return RLIST
def scoreList(ID,MATCHLIST,D1SCORE,D2SCORE,D3SCORE,D4SCORE,D5SCORE):
        STIME=time.time()
        NLIST=[]
	D1RAT=float(D1SCORE-D2SCORE)/D2SCORE*100
	D2RAT=float(D2SCORE-D3SCORE)/D3SCORE*100
	D3RAT=float(D3SCORE-D4SCORE)/D4SCORE*100
	D4RAT=float(D4SCORE-D5SCORE)/D5SCORE*100
	D5RAT=float(D5SCORE-D1SCORE)/D1SCORE*100
        for m in MATCHLIST:
		M1RAT=float(m[DATE1]-m[DATE2])/m[DATE2]*100
		M2RAT=float(m[DATE2]-m[DATE3])/m[DATE3]*100
		M3RAT=float(m[DATE3]-m[DATE4])/m[DATE4]*100
		M4RAT=float(m[DATE4]-m[DATE5])/m[DATE5]*100
		M5RAT=float(m[DATE5]-m[DATE1])/m[DATE1]*100
		try:
			TOTDIFF=math.fabs(math.fabs(M1RAT/D1RAT)+math.fabs(M2RAT/D2RAT)+math.fabs(M3RAT/D3RAT)+math.fabs(M4RAT/D4RAT)+math.fabs(M5RAT/D5RAT))
		except ZeroDivisionError:
			print 'zde error for '+str(m['title'])
			break
                rec={'_id':m['_id'],'title':m['title'],'TOTAL':float(str(TOTDIFF)[0:5])}
		if m['_id']!=ID:
	                NLIST.append(rec)
        ETIME=time.time()
        TTIME=ETIME-STIME
        print 'scoring done in '+str(TTIME)+' seconds.'
        return NLIST


STARTTIME=time.time()
MATCHLIST=getDayList()
ENDTIME=time.time()
TTIME=ENDTIME-STARTTIME
print "found "+ str(len(MATCHLIST))+" records in "+str(TTIME)+" seconds, now scoring..."

COUNT=0
ENTHREE=db['en_threehour'].find()
for m in ENTHREE:
        ID=m['id']
        TITLE=m['title']
        D1Q=db[HD].find_one({'_id':ID})
        try:
                try:
			D1SCORE=D1Q[DATE1]
		except KeyError:
			D1SCORE=1
                try:
			D2SCORE=D1Q[DATE2]
		except KeyError:
			D2SCORE=1
		try:
	                D3SCORE=D1Q[DATE3]
		except KeyError:
			D3SCORE=1
		try:
	                D4SCORE=D1Q[DATE4]
		except KeyError:
			D4SCORE=1
		try:
	                D5SCORE=D1Q[DATE5]
		except KeyError:
			D5SCORE=1

                NEWLIST=scoreList(ID,MATCHLIST,D1SCORE,D2SCORE,D3SCORE,D4SCORE,D5SCORE)
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
			nrec={'Pid':str(ID),'id':str(rec[1]),'title':str(rec[2]),'score':str(rec[0])[0:5]}
        		LC+=1
			db[SD].insert(nrec)
        except KeyError:
                print 'keyError for '+str(TITLE)




