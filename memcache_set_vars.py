#!/usr/bin/python
import memcache 
import string 
import urllib2
import random
from pymongo import Connection
from datetime import date

#conn=Connection('10.245.145.84')
conn=Connection('10.115.126.7')
db=conn.wc
mc=memcache.Client(['127.0.0.1:11211'],debug=0)
TODAY=date.today()
DAY=TODAY.day
MONTH=TODAY.month
YEAR=TODAY.year

DAILYPAGERESULTS=db.command({'distinct':'tophits','key':'d','query':{'m':int(MONTH)}})
def Query_NewsFind(FINDQUERY,notedate,notes):
        findresults=db.news.find(FINDQUERY)
        for a in findresults:
                notedate=a['date']
                notes=a['text']

        return
def MapQuery_FindName(id):
        QUERY={'id':id}
        MAPQ=db.hits.find({'_id':id})
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

def GenInfoPage(id):
	QUERY={'id':id}
	FINDQ=db.tophits.find(QUERY).sort([('y',1),('m',1),('d',1)])
	INFOVIEW_KEY='infoview_'+str(id)
	send_list=[]
        for result in FINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
        	send_list.append(rec)
        mc.set(INFOVIEW_KEY,send_list,60*60*12)
	return


send_list=[]
print 'daily pages first....'
for d in DAILYPAGERESULTS['values']:
	rec={'d':d,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(d)}
        send_list.append(rec)
mc.set('mcdpDaysList',send_list,60*60*24)



QUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
send_list=[]
RESULTSET=db.tophits.find(QUERY).sort('place',1).limit(100)
for row in RESULTSET:
	GenInfoPage(row['id'])
	title,utitle=FormatName(row['title'])
        rec={'place':row['place'],'Hits':row['Hits'],'title':utitle ,'id':str(row['id']),'linktitle':title.encode('utf-8')}
        send_list.append(rec)
mc.set('DAYKEY',send_list,7200)
notedate=''
notes=''
latest_hits_list = db.tophits.find(QUERY).sort('place',1).limit(100)
for p in latest_hits_list:
	GenInfoPage(p['id'])
        title,utitle=FormatName(p['title'])
	rec={'title':utitle,'place':p['place'],'Hits':p['Hits']%1000,'linktitle':title.encode('utf-8'),'notedate':notedate,'notes':notes,'id':p['id']}
        send_list.append(rec)
mc.set('send_list',send_list,3600)


print 'now trending list query....'
send_list=[]    
TRENDING_LIST_QUERY=db.prodtrend.find().sort('Hits',-1).limit(50)
for p in TRENDING_LIST_QUERY:
	rec={'title':p['title'],'place':p['place'],'Hits':p['Hits']%1000,'linktitle':p['linktitle'],'id':p['id']}
        send_list.append(rec)
	GenInfoPage(p['id'])
mc.set('TRENDING_LIST_QUERY',send_list,1800)


print 'random query...'
send_list=[]
for a in range(1,50):
	place=random.randint(1,250000)
        FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR),'place':place}
        RANDOM_LIST_QUERY=db.tophits.find(FQUERY)
        for item in RANDOM_LIST_QUERY:
        	 id=item['id']
		 GenInfoPage(item['id'])
       		 title,utitle=FormatName(item['title']) 
        	 rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':title.encode('utf-8'),'id':item['id']}
        	 send_list.append(rec)
mc.set('RANDOM_ARTICLES',send_list,60*60)


print 'debuts query...'
send_list=[]
title=''
utitle=''
QUERY=db.proddebuts.find({'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}).limit(100)
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
RESULTSET=db.command({'distinct':'tophits','key':'d','query':{'m':int(MONTH),'y':int(YEAR)}})
for d in RESULTSET['values']:
	rec={'d':d,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(d)}
	QUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	DAYKEY='toplist'+str(YEAR)+str(MONTH)+str(DAY)
	page_list=[]
        PAGERESULTSET=db.tophits.find(QUERY).sort('place',1).limit(100)
        for row in PAGERESULTSET:
		title, utitle=FormatName(row['title'])
                prec={'place':row['place'],'Hits':row['Hits'],'title':title ,'id':str(row['id']),'linktitle':utitle}
                page_list.append(prec)
                mc.set('DAYKEY',page_list,60*60*24*14)
        send_list.append(rec)
mc.set('mcdpDaysList'+str(MONTH)+str(YEAR),send_list,60*60*24)

#print 'on to dec 2012 archives...'
#send_list=[]
#RESULTSET=db.command({'distinct':'tophits','key':'d','query':{'m':12}})
#for d in RESULTSET['values']:
#	rec={'d':d,'m':12,'y':2012,'stry':str(2012),'strm':str(12),'strd':str(d)}
#	QUERY={'d':int(DAY),'m':int(12),'y':int(2012)}
#	DAYKEY='toplist'+str(2012)+str(12)+str(DAY)
#	page_list=[]
 #       PAGERESULTSET=db.tophits.find(QUERY).sort('place',1).limit(100)
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
for p in THREEHOUR_LIST_QUERY:
	rec={'title':p['title'],'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id']}
        send_list.append(rec)
mc.set('THREEHOUR_LIST_QUERY',send_list,60*60) 

