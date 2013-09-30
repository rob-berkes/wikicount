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
DATE3="2013_09_04"
DATE4="2013_08_29"



def makeArray(LLIST):
        NEWARRAY=[]
        for i in LLIST:
                rec=(i['TOTAL'],i['_id'],i['title'])
                NEWARRAY.append(rec)
        return NEWARRAY
        
def getDayList():
        print 'building array'
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
        print 'scoring array'
        STIME=time.time()
        NLIST=[]
	D1RAT=float(D1SCORE-D2SCORE)/D2SCORE*100
	D2RAT=float(D2SCORE-D3SCORE)/D3SCORE*100
	print D1RAT,D1SCORE,D2SCORE
	print 'D1RAT= '+str(D1RAT)
        for m in MATCHLIST:
		M1RAT=float(m[DATE1]-m[DATE2])/m[DATE2]*100
		M2RAT=float(m[DATE2]-m[DATE3])/m[DATE3]*100
		try:
			TOTDIFF=math.fabs(float(M1RAT/D1RAT)*1000+float(M2RAT/D2RAT)*1000)
		except ZeroDivisionError:
			print 'zde error for '+str(m['title'])
			continue
                rec={'_id':m['_id'],'title':m['title'],'TOTAL':float(TOTDIFF)}
		if m['_id']!=ID:
	                NLIST.append(rec)
        ETIME=time.time()
        TTIME=ETIME-STIME
        print 'scoring done in '+str(TTIME)+' seconds.'
        return NLIST

def smpScoFunction(ML,cconn,D1SCORE,D2SCORE,D3SCORE,D4SCORE):
        print 'entered scoFunc'
        NL=[]
        for i in ML:
                try:
                        D1DIFF=math.fabs(D1SCORE-i[DATE1])
                        D2DIFF=math.fabs(D2SCORE-i[DATE2])
                        D3DIFF=math.fabs(D3SCORE-i[DATE3])
                        D4DIFF=math.fabs(D4SCORE-i[DATE4])
                        TOTDIFF=D1DIFF+D2DIFF+D3DIFF
                        if i['_id']!=ID:
                                rec={'_id':i['_id'],'title':i['title'],'D1DIFF':D1DIFF,'D2DIFF':D2DIFF,'D3DIFF':D3DIFF,'TOTAL':TOTDIFF}
                                NL.append(rec)
                except KeyError:
                        print 'keyError'
                        pass
        cconn.send(NL)
        print 'end scoFunc reached'
        
        return
def smpScore(M1,M2,M3,D1SCORE,D2SCORE,D3SCORE,D4SCORE):
        st=time.time()
        pconn,cconn=Pipe()
        qconn,dconn=Pipe()
        rconn,econn=Pipe()
        nLIST=[]

        p=Process(target=smpScoFunction,args=(M1,cconn,D1SCORE,D2SCORE,D3SCORE,D4SCORE))
        q=Process(target=smpScoFunction,args=(M2,dconn,D1SCORE,D2SCORE,D3SCORE,D4SCORE))
        r=Process(target=smpScoFunction,args=(M3,econn,D1SCORE,D2SCORE,D3SCORE,D4SCORE))

        p.start()
        q.start()
        r.start()
        
        p1LIST=pconn.recv()     
        p2LIST=qconn.recv()
        p3LIST=rconn.recv()

        
        p.join()
        q.join()
        r.join()
        
        nLIST=p1LIST+p2LIST+p3LIST
        et=time.time()
        tt=et-st
        print 'smp scoring done in '+str(tt)+' seconds.'
        return nLIST    
def splitInThree(MATCHLIST):
        st=time.time()
        M1=[]
        M2=[]
        M3=[]
        M4=[]
        COUNT=1
        for item in MATCHLIST:
                if COUNT==1:
                        COUNT+=1
                        M1.append(item)
                elif COUNT==2:
                        COUNT+=1
                        M2.append(item)
                elif COUNT==3:
                        COUNT=1
                        M3.append(item)
                else:
                        COUNT=1
                        M3.append(item)
        et=time.time()
        tt=et-st
        print 'split in 3 in '+str(tt)+' seconds.'
        return M1,M2,M3

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
                D1SCORE=D1Q[DATE1]
                D2SCORE=D1Q[DATE2]
                D3SCORE=D1Q[DATE3]
                D4SCORE=D1Q[DATE4]
                NEWLIST=scoreList(ID,MATCHLIST,D1SCORE,D2SCORE,D3SCORE,D4SCORE)
                st=time.time()
                NEWARRAY=makeArray(NEWLIST)
                et=time.time()
                tt=et-st
                print 'array made in '+str(tt)+' seconds.'
                st=time.time()
                SORTLIST=sorting.QuickSortListArray(NEWARRAY)
                et=time.time()
                tt=et-st
                print 'sorting done in '+str(tt)+' seconds.'
		try:
	        	OFILE=open('/tmp/django/wikicount/static/images/'+str(lang)+'/similar/'+str(ID)+'.htm','w')
		except IOError:
			os.makedirs('/tmp/django/wikicount/static/images/'+str(lang)+'/similar/')
			OFILE=open('/tmp/django/wikicount/static/images/'+str(lang)+'/similar/'+str(ID)+'.htm','w')
                LC=1
                for rec in SORTLIST:
                        if LC>11:
                                break
                        OFILE.write('<li>('+str(rec[0])+')<a href="http://www.wikitrends.info/'+str(lang)+'infoview/'+str(rec[1])+'> '+str(rec[2])+'</a></li><br>')
                        OFILE.write('\n')
                        LC+=1
                OFILE.close()
        except TypeError:
                print 'typeError for '+str(TITLE)
        except KeyError:
                print 'keyError for '+str(TITLE)




