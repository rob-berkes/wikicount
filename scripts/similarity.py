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
DATE1="2013_09_29"
DATE2="2013_09_28"
DATE3="2013_09_27"
DATE4="2013_09_25"



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
def scoreList(ID,MATCHLIST,D1SCORE,D2SCORE,D3SCORE,D4SCORE):
        STIME=time.time()
        NLIST=[]
	D1RAT=float(D1SCORE-D2SCORE)/D2SCORE*100
	D2RAT=float(D2SCORE-D3SCORE)/D3SCORE*100
        for m in MATCHLIST:
		M1RAT=float(m[DATE1]-m[DATE2])/m[DATE2]*100
		M2RAT=float(m[DATE2]-m[DATE3])/m[DATE3]*100
		try:
			TOTDIFF=float(math.fabs(M1RAT/D1RAT)+math.fabs(M2RAT/D2RAT))
		except ZeroDivisionError:
			print 'zde error for '+str(m['title'])
			break
                rec={'_id':m['_id'],'title':m['title'],'TOTAL':TOTDIFF}
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

                NEWLIST=scoreList(ID,MATCHLIST,D1SCORE,D2SCORE,D3SCORE,D4SCORE)
                NEWARRAY=makeArray(NEWLIST)
	
		st=time.time()
                SORTLIST=sorting.QuickSortListArray(NEWARRAY,'asc')
		et=time.time()
		tt=et-st
		print 'list sorted in '+str(tt)+' seconds.'

		try:
	        	OFILE=open('/tmp/django/wikicount/static/images/'+str(lang)+'/similar/'+str(ID)+'.htm','w')
		except IOError:
			os.makedirs('/tmp/django/wikicount/static/images/'+str(lang)+'/similar/')
			OFILE=open('/tmp/django/wikicount/static/images/'+str(lang)+'/similar/'+str(ID)+'.htm','w')
        except TypeError:
                print 'typeError for '+str(TITLE)
        except KeyError:
                print 'keyError for '+str(TITLE)
        LC=1
	db[SD].remove({'_id':ID})
	SDLIST=[]
	OFILE.write('<li>----------------'+str(TITLE)+'-----------------</li><br>\n')
        for rec in SORTLIST:
        	if LC>11:
                	break
		nrec={'id':str(rec[1]),'title':str(rec[2]),'score':rec[0]}
		SDLIST.append(nrec)
        	OFILE.write('<li>('+str(rec[0])+')<a href="http://www.wikitrends.info/'+str(lang)+'/infoview/'+str(rec[1])+'> '+str(rec[2])+'</a></li><br>')
        	OFILE.write('\n')
        	LC+=1
		db[SD].update({'_id':str(ID)},{'$set':{'similars':SDLIST}},upsert=True)
        OFILE.close()




