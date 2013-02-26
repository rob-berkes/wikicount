#!/usr/bin/python
import memcache 
import string 
import urllib2
import random
from pymongo import Connection
from datetime import date
from datetime import time
import datetime
import subprocess
import syslog
import os

#conn=Connection('10.245.145.84')
conn=Connection('10.115.126.7')
db=conn.wc
mc=memcache.Client(['127.0.0.1:11211'],debug=0)
TODAY=date.today()
DAY=TODAY.day
MONTH=TODAY.month
YEAR=TODAY.year
MONTHNAME=datetime.datetime.now().strftime("%B")
thCN='tophits'+str(YEAR)+MONTHNAME
dbCN='proddebuts'+str(YEAR)+str(MONTHNAME)
DAILYPAGERESULTS=db.command({'distinct':thCN,'key':'d','query':{'m':int(MONTH)}})

def latestnews():
        ARTICLELIMIT=5
        latest_news_list = db.news.find().sort('date',-1).limit(ARTICLELIMIT)
        return latest_news_list


def Query_NewsFind(FINDQUERY,notedate,notes):
        findresults=db.news.find(FINDQUERY)
        for a in findresults:
                notedate=a['date']
                notes=a['text']

        return
def MapQuery_FindName(id):
        QUERY={'id':id}
        MAPQ=db.hitsdaily.find({'_id':id})
        latest_news_list = latestnews()
        title=''
        utitle=''
        for name in MAPQ:
                        title=name['title']
                        s_title=string.replace(title,'_',' ')
                        t_title=s_title.encode('utf-8')
                        utitle=urllib2.unquote(t_title)


        return title, utitle
def FormatName(title):
        s_title=string.replace(title,'_',' ')
        t_title=s_title.encode('utf-8')
        utitle=urllib2.unquote(t_title)
        return title, utitle

def returnHourString(hour):
	HOUR='%02d' % (hour,)
	return HOUR
def GenHourlyGraph(id):
	RESULT1=db.hitshourly.find_one({"_id":str(id)})
	OFILE=open('output.log','w')
	try:
		for i in range(0,24):
			HOUR=returnHourString(i)	
			try:
				OFILE.write(str(HOUR)+' '+str(RESULT1[HOUR])+'\n')
			except TypeError:
				pass 
	except KeyError:
		pass
	OFILE.close()
	subprocess.call(["gnuplot","gnuplot.plot"])
	OUTFILENAME='/tmp/django/wikicount/static/images/hourly/'+str(id)+'.png'
	SFILE='/tmp/django/wikicount/introduction.png'
	subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	return
def GenInfoPage(id):
	GenHourlyGraph(id)
	MONTHNAME=datetime.datetime.now().strftime("%B")
	thCN='tophits'+str(YEAR)+MONTHNAME
	QUERY={'id':id}
	Q50K={'id':id,'place':{'$lt':50001}}
	Q5K={'id':id,'place':{'$lt':5001}}
	Q500={'id':id,'place':{'$lt':501}}
	Q50={'id':id,'place':{'$lt':51}}
	FINDQ=db[thCN].find(QUERY)
	DFINDQ=db.tophits.find(QUERY)
	D50KFINDQ=db.tophits.find(Q50K)
	D5KFINDQ=db.tophits.find(Q5K)
	D500FINDQ=db.tophits.find(Q500)
	D50FINDQ=db.tophits.find(Q50)
	INFOVIEW_KEY='infoview_'+str(id)
	INFOVIEWLT_KEY='infoviewlt_'+str(id)
	INFOVIEWLT5K_KEY='infoviewlt5k_'+str(id)
	INFOVIEWLT500_KEY='infoviewlt500_'+str(id)
	INFOVIEWLT50_KEY='infoviewlt50_'+str(id)
	send_list=[]
	info_lt50k_list=[]
	info_lt5k_list=[]
	info_lt500_list=[]
	info_lt50_list=[]
        
	OFILE250K=open("/tmp/t250k.log","w")	
	for result in DFINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE250K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	send_list.append(rec)
        for result in FINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE250K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	send_list.append(rec)
	OFILE250K.close()
	OUTFILENAME='/tmp/django/wikicount/static/images/t250k/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.250k"])
		SFILE='/tmp/t250k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.250k"])
		SFILE='/tmp/t250k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
			
	OFILE50K=open("/tmp/t50k.log","w")	
	LT50KQ=db[thCN].find(Q50K)
        for result in D50KFINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE50K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt50k_list.append(rec)
        for result in LT50KQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE50K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt50k_list.append(rec)
	OFILE50K.close()
	OUTFILENAME='/tmp/django/wikicount/static/images/t50k/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.50k"])
		SFILE='/tmp/t50k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.50k"])
		SFILE='/tmp/t50k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)

	OFILE5K=open("/tmp/t5k.log","w")	
	LT5KQ=db[thCN].find(Q5K)
        for result in D5KFINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE5K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt5k_list.append(rec)
        for result in LT5KQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE5K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt5k_list.append(rec)
	OFILE5K.close()
	OUTFILENAME='/tmp/django/wikicount/static/images/t5k/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.5k"])
		SFILE='/tmp/t5k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.5k"])
		SFILE='/tmp/t5k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)

	LT500=db[thCN].find(Q500)
	OFILE500=open("/tmp/top500.log","w")
        for result in D500FINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE500.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt500_list.append(rec)
        for result in LT500:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE500.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt500_list.append(rec)
	OFILE500.close()	
	OUTFILENAME='/tmp/django/wikicount/static/images/t500/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.500"])
		SFILE='/tmp/top500.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.500"])
		SFILE='/tmp/top500.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)

	LT50=db[thCN].find(Q50)
	OFILE50=open("/tmp/top50.log","w")
        for result in D50FINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE50.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt50_list.append(rec)
        for result in LT50:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE50.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt50_list.append(rec)
	OFILE50.close()	
	OUTFILENAME='/tmp/django/wikicount/static/images/t50/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.50"])
		SFILE='/tmp/top50.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.50"])
		SFILE='/tmp/top50.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)


        mc.set(INFOVIEW_KEY,send_list,60*60*12)
	mc.set(INFOVIEWLT_KEY,info_lt50k_list,60*60*12)
	mc.set(INFOVIEWLT5K_KEY,info_lt5k_list,60*60*12)
	mc.set(INFOVIEWLT500_KEY,info_lt500_list,60*60*12)
	mc.set(INFOVIEWLT50_KEY,info_lt50_list,60*60*12)
	return


send_list=[]
print 'daily pages first....'
for d in DAILYPAGERESULTS['values']:
	rec={'d':d,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(d)}
        send_list.append(rec)
mc.set('mcdpDaysList',send_list,60*60*24)



QUERY={'d':DAY,'m':MONTH,'y':YEAR}
send_list=[]
RESULTSET=db[thCN].find(QUERY).sort('place',1).limit(100)
syslog.syslog('memcache-daily: '+str(QUERY)+' count: '+str(RESULTSET.count()))
for row in RESULTSET:
	GenInfoPage(row['id'])
	title,utitle=FormatName(row['title'])
        rec={'place':row['place'],'Hits':row['Hits'],'title':utitle ,'id':str(row['id']),'linktitle':title.encode('utf-8')}
        send_list.append(rec)
mc.set('DAYKEY',send_list,7200)
notedate=''
notes=''
latest_hits_list = db[thCN].find(QUERY).sort('place',1).limit(100)
syslog.syslog('memcache-latest: '+str(QUERY)+' count: '+str(latest_hits_list.count()))
for p in latest_hits_list:
	GenInfoPage(p['id'])
        title,utitle=FormatName(p['title'])
	rec={'title':utitle,'place':p['place'],'Hits':p['Hits']%1000,'linktitle':title.encode('utf-8'),'notedate':notedate,'notes':notes,'id':p['id']}
        send_list.append(rec)
mc.set('send_list',send_list,3600)


send_list=[]    
TRENDING_LIST_QUERY=db.prodtrend.find({u'd':DAY,u'm':MONTH,u'y':YEAR}).sort('Hits',-1).limit(150)
syslog.syslog('memcache-trending: '+str(QUERY)+' count: '+str(TRENDING_LIST_QUERY.count()))
print TRENDING_LIST_QUERY.count()
for p in TRENDING_LIST_QUERY:
	rec={'title':p['title'],'place':p['place'],'Hits':p['Hits']%1000,'linktitle':p['linktitle'],'id':p['id']}
        send_list.append(rec)
	GenInfoPage(p['id'])
mc.set('TRENDING_LIST_QUERY',send_list,1800)


print 'random query...'
send_list=[]
for a in range(1,50):
	place=random.randint(1,250000)
        FQUERY={u'd':DAY,u'm':MONTH,u'y':YEAR,'place':place}
        RANDOM_LIST_QUERY=db[thCN].find(FQUERY)
        for item in RANDOM_LIST_QUERY:
        	 id=item['id']
		 GenInfoPage(item['id'])
       		 title,utitle=FormatName(item['title']) 
        	 rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':title.encode('utf-8'),'id':item['id']}
        	 send_list.append(rec)
mc.set('RANDOM_ARTICLES',send_list,60*60)


HOUR=datetime.datetime.now().strftime('%H')
print 'debuts query...'
send_list=[]
title=''
utitle=''
QUERY=db[dbCN].find({u'd':DAY,u'm':MONTH,u'y':YEAR}).sort('place',1).limit(300)
syslog.syslog('memcache-debuts: count: '+str(QUERY.count()))
for item in QUERY:
	COUNT=0
        TITLE=''
	GenInfoPage(item['id'])
	title,utitle=FormatName(item['title'])

	rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':item['linktitle'],'id':item['id']}
        send_list.append(rec)
mc.set('DEBUTS_ARTICLES',send_list,60*60)


print 'current month archive...'
send_list=[]
RESULTSET=db.command({'distinct':thCN,'key':'d','query':{'m':int(MONTH),'y':int(YEAR)}})
for d in RESULTSET['values']:
	rec={'d':d,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(d)}
	QUERY={'d':int(d),'m':int(MONTH),'y':int(YEAR)}
	DAYKEY='toplist'+str(YEAR)+str(MONTH)+str(DAY)
	page_list=[]
        PAGERESULTSET=db[thCN].find(QUERY).sort('place',1).limit(100)
	syslog.syslog('memcache-monthly: '+str(d)+' '+str(QUERY)+' count: '+str(PAGERESULTSET.count()))
        for row in PAGERESULTSET:
		title, utitle=FormatName(row['title'])
                prec={'place':row['place'],'Hits':row['Hits'],'title':title ,'id':str(row['id']),'linktitle':utitle}
		GenInfoPage(row['id'])
                page_list.append(prec)
                mc.set('DAYKEY',page_list,60*60*24*14)
        send_list.append(rec)
mc.set('mcdpDaysList'+str(MONTH)+str(YEAR),send_list,60*60*24)

#print 'on to dec 2012 archives...'
#send_list=[]
#RESULTSET=db.command({'distinct':thCN,'key':'d','query':{'m':12}})
#for d in RESULTSET['values']:
#	rec={'d':d,'m':12,'y':2012,'stry':str(2012),'strm':str(12),'strd':str(d)}
#	QUERY={'d':int(DAY),'m':int(12),'y':int(2012)}
#	DAYKEY='toplist'+str(2012)+str(12)+str(DAY)
#	page_list=[]
 #       PAGERESULTSET=db[thCN].find(QUERY).sort('place',1).limit(100)
#$        for row in PAGERESULTSET:
#		title, utitle=FormatName(row['title'])
 #               prec={'place':row['place'],'Hits':row['Hits'],'title':title ,'id':str(row['id']),'linktitle':utitle}
#                page_list.append(prec)
#                mc.set('DAYKEY',page_list,60*60*24*14)
#        send_list.append(rec)
#mc.set('mcdpDaysList'+str(12)+str(2012),send_list,60*60*24)

print 'lastly, 3hr rolling average'
send_list=[]
THREEHOUR_LIST_QUERY=db.threehour.find().sort('place',1)
syslog.syslog('memcache-threehour:  count: '+str(THREEHOUR_LIST_QUERY.count()))
for p in THREEHOUR_LIST_QUERY:
	rec={'title':p['title'],'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id']}
	GenInfoPage(p['id'])
        send_list.append(rec)
mc.set('THREEHOUR_LIST_QUERY',send_list,60*60) 



SEARCH_HOUR='%02d' % (int(HOUR),)
HOURQUERY=db.hitshourlydaily.find({str(SEARCH_HOUR):{'$gt':1}}).sort(str(SEARCH_HOUR),-1).limit(50)
send_list=[]
place=1
HOURKEY="SEARCHHOUR_"+str(SEARCH_HOUR)
syslog.syslog('memcache-hourly: '+' count: '+str(HOURQUERY.count()))
for row in HOURQUERY:
    title,utitle=MapQuery_FindName(row['_id'])
    GenInfoPage(row['_id'])
    rec={'place':place,'Hits':row[str(SEARCH_HOUR)],'title':utitle ,'id':str(row['_id']),'linktitle':title.encode('utf-8')}
    place+=1
    send_list.append(rec)
mc.set(HOURKEY,send_list,30*60)

