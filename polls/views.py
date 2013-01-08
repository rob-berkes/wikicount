from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.cache import cache_page
from pymongo import Connection
from datetime import date
import urllib2
import string
import random
import datetime
import hashlib
import memcache
from wsgiref.handlers import format_date_time
from time import mktime
import time
import tweepy 
import syslog

conn=Connection('10.195.138.15')
#conn=Connection('10.80.121.190')
#conn=Connection()
db=conn.wc
api=tweepy.api
RECORDSPERPAGE=50
mc=memcache.Client(['127.0.0.1:11211'],debug=0)




#All purpose Functions

def ReturnHexDigest(article):
	hd=hashlib.sha1(article).hexdigest()
	return hd
def latestnews():
	ARTICLELIMIT=5
	latest_news_list = db.news.find().sort('date',-1).limit(ARTICLELIMIT)
	return latest_news_list
def MapQuery_FindName(id):
	QUERY={'id':id}
        MAPQ=db.map.find({'_id':id})
        latest_news_list = latestnews()
	title=''
	utitle=''
        for name in MAPQ:
                        title=name['title']
                        s_title=string.replace(title,'_',' ')
                        t_title=s_title.encode('utf-8')
                        utitle=urllib2.unquote(t_title)


	return title, utitle
def GetTimeline():
	status=api.user_timeline('wikitrendsinfo',count=5)


	return status
def Query_NewsFind(FINDQUERY,notedate,notes):
	findresults=db.news.find(FINDQUERY)
	for a in findresults:
		notedate=a['date']
		notes=a['text']

	return
def fnReturnTimes():
        TODAY=date.today()
        YEAR=TODAY.year
        DAY=TODAY.day
        MONTH=TODAY.month
        now=datetime.datetime.now()
        half=now+datetime.timedelta(minutes=45)
        stamp=mktime(half.timetuple())
        expiretime=format_date_time(stamp)
        if DAY==0:
           DAY=30
           MONTH-=1
        if MONTH==0:
           DAY=31
           MONTH=12
           YEAR-=1
	HOUR=time.strftime('%H')
	return DAY, MONTH, YEAR,HOUR, expiretime

def GenArchiveList():
	archive_list=[]
	dec12={'text':'Dec 2012','d': '31','m':'12','y':'2012'}
	archive_list.append(dec12)
	return archive_list
	

def adjustHourforLastHour(HOUR):
	SEARCH_HOUR=int(HOUR)+4
        if SEARCH_HOUR == 27:
                SEARCH_HOUR = 3  
        elif SEARCH_HOUR == 26:
                SEARCH_HOUR = 2
        elif SEARCH_HOUR == 25:
                SEARCH_HOUR = 1
	elif SEARCH_HOUR == 24:
		SEARCH_HOUR = 0
	return SEARCH_HOUR





#Begin application functions

def listLastHour(request):
	DAY,MONTH,YEAR,HOUR,expiretime=fnReturnTimes()
	tw_timeline=GetTimeline()
	t=get_template('IndexListLast.html')
	latest_news_list=latestnews()
	SEARCH_HOUR=adjustHourforLastHour(HOUR)
	HOURQUERY=db.hitshourly.find().sort(str(SEARCH_HOUR),-1).limit(50)
	send_list=[]
	place=1
	HOURKEY="SEARCHHOUR_"+str(SEARCH_HOUR)
	send_list=mc.get(HOURKEY)
	if send_list:
		pass
	else:
		for row in HOURQUERY:
			title,utitle=MapQuery_FindName(row['_id'])		 	
			rec={'place':place,'Hits':row[str(SEARCH_HOUR)],'title':utitle ,'id':str(row['_id']),'linktitle':title.encode('utf-8')}
			place+=1
			send_list.append(rec)
	mc.set(HOURKEY,send_list,30*60)
	c=Context({'latest_hits_list':send_list,'latest_news_list':latest_news_list,'y':YEAR,'m':MONTH,'d':DAY,'tw_timeline':tw_timeline,'latest_news_list':latest_news_list})
	rendered=t.render(c)
	return HttpResponse(rendered)
	
def searchResults(request):
	title=''
	if 'q' in request.GET:
		message="You searched for "+request.GET['q']
		title=request.GET['q'].decode('utf-8')
		etitle=title.encode('utf-8')
		stitle=string.replace(etitle,' ','_')
	else:
		message="You submitted an empty query"
	DAY,MONTH,YEAR,HOUR,expiretime=fnReturnTimes()
	hd=ReturnHexDigest(stitle)
	title,utitle=MapQuery_FindName(hd)
	t=get_template('IndexSearchResults.html')
	MAPQ={'_id': str(hd)}
	MAPQUERY=db.map.find(MAPQ).limit(20)
	send_list=[]
	print MAPQ
	infoview(request,hd)
	for item in MAPQUERY:
		rec={'id':str(item['_id']),'title':str(item['title']),'linktitle':utitle}
		print rec
		send_list.append(rec)
	c=Context({'news_list':send_list,'expiretime':expiretime})
	rendered=t.render(c)
	return HttpResponse(rendered)
	

def searchForm(request):
	DAY,MONTH,YEAR,HOUR,expiretime=fnReturnTimes()
	t=get_template('IndexSearch.html')
	send_list=[]
	c=Context({expiretime:expiretime})
	rendered=t.render(c)
	return HttpResponse(rendered)


def blog(request):
	DAY,MONTH,YEAR,HOUR,expiretime=fnReturnTimes()
	BLOGQUERY=db.blog.find().sort('date',-1).limit(10)
	t=get_template('IndexBlog.html')
	send_list=[]
	title=''
	for p in BLOGQUERY:
		rec={'newsdate':p['date'],'headtext':p['text']}
		print rec
		send_list.append(rec)
	c=Context({'news_list':send_list,expiretime:expiretime})
	rendered=t.render(c)
	return HttpResponse(rendered)


def dailypage(request,YEAR=2013,MONTH=1):
	syslog.syslog('wc-dailypage MONTH='+str(MONTH))
	junk1,junk2,junk3,junk4,expiretime=fnReturnTimes()
	t=get_template('IndexDaily.html')
	send_list=mc.get('mcdpDaysList'+str(MONTH)+str(YEAR))
	archive_list=GenArchiveList()
	if send_list:
		pass
	else:
		send_list=[]
		RESULTSET=db.command({'distinct':'tophits','key':'d','query':{'m':int(MONTH),'y':int(YEAR)}})
		for d in RESULTSET['values']:
			rec={'d':d,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(d)}
			print rec
			send_list.append(rec)
		mc.set('mcdpDaysList'+str(MONTH)+str(YEAR),send_list,60*60*24)

	title=''
	c=Context({'news_list':send_list,expiretime:expiretime,'archive_list':archive_list})
	rendered=t.render(c)
	return HttpResponse(rendered)


def listtop(request,YEAR,MONTH,DAY):
	t=get_template('IndexTopList.html')
	send_list=[]
	#print request
	QUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	DAYKEY='toplist'+str(YEAR)+str(MONTH)+str(DAY)
	syslog.syslog('wikicount-views.py-listtop DAYKEY='+DAYKEY)
	print QUERY
	send_list=mc.get(DAYKEY)
	tw_timeline=GetTimeline()
	latest_news_list=latestnews() 
	if send_list:
		pass
	else:
		send_list=[]
		RESULTSET=db.tophits.find(QUERY).sort('place',1).limit(100)
		for row in RESULTSET:
			title=''
			utitle=''
			MAPQUERY={'_id':row['id']}
			MAPRESULT=db.map.find(MAPQUERY)
			for name in MAPRESULT:
	                                title=name['title']
	                                s_title=string.replace(title,'_',' ')
	                                t_title=s_title.encode('utf-8')
	                                utitle=urllib2.unquote(t_title)
			rec={'place':row['place'],'Hits':row['Hits'],'title':utitle ,'id':str(row['id']),'linktitle':title.encode('utf-8')}
			send_list.append(rec)
		mc.set('DAYKEY',send_list,7200)
	c=Context({'latest_hits_list':send_list,'y':YEAR,'m':MONTH,'d':DAY,'tw_timeline':tw_timeline,'latest_news_list':latest_news_list})
	rendered=t.render(c)
	return HttpResponse(rendered)


def debug(request):
	DAY, MONTH, YEAR, HOUR,expiretime = fnReturnTimes()
	t=get_template('RedTieIndex.html')
	notedate=''
	notes=''
	FINDQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	print FINDQUERY
	latest_hits_list = db.prodtop.find().sort('place',1).limit(50)
	send_list=[]
	title=''
	for p in latest_hits_list:
		mapped_name=db.map.find(QUERY)
		for name in mapped_name:
			title=name['title']
			s_title=string.replace(title,'_',' ')
			t_title=s_title.encode('utf-8')
			utitle=urllib2.unquote(t_title)
		rec={'title':utitle,'place':p['place'],'Hits':p['Hits'],'linktitle':title.encode('utf-8'),'notedate':notedate,'notes':notes,'id':p['id']}
			
		send_list.append(rec)
	c=Context({'latest_hits_list':send_list,'latest_news_list':latest_news_list,'PageTitle':'WikiTrends.Info - Top Pages','PageDesc':'Wikipedia\'s most popular pages, updated every 2 hours or so.','expiretime':expiretime})
	rendered=t.render(c)
	return HttpResponse(rendered)


def infoview(request,id):
	DAY, MONTH, YEAR, HOUR,expiretime = fnReturnTimes()
        QUERY={'id':id}
	FINDQ=db.tophits.find(QUERY).sort([('y',1),('m',1),('d',1)])
	INFOVIEW_KEY='infoview_'+str(id)
	latest_news_list = latestnews()
	
	tw_timeline=GetTimeline() 
	send_list=mc.get(INFOVIEW_KEY)
	if send_list:
		pass
	else:
		send_list=[]
		for result in FINDQ:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			send_list.append(rec)
		mc.set(INFOVIEW_KEY,send_list,60*24*24)
	title, utitle = MapQuery_FindName(id)
	t=get_template('InfoviewIndex.htm')
	c=Context({'info_find_query':send_list,'latest_news_list':latest_news_list,'PageTitle':utitle,'expiretime':expiretime,'linktitle':title,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)


def trending(request):
	DAY, MONTH, YEAR, HOUR,expiretime = fnReturnTimes()
	mcHour=mc.get('trendingHour')
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	print FQUERY
	LATEST_NEWS_LIST=latestnews()
	title=''
	send_list=mc.get('TRENDING_LIST_QUERY')
	tw_timeline=GetTimeline() 
	if send_list:
		pass
	else:	
		send_list=[]	
		TRENDING_LIST_QUERY=db.prodtrend.find().sort('Hits',-1).limit(50)
		for p in TRENDING_LIST_QUERY:
			rec={'title':p['title'],'place':p['place'],'Hits':p['Hits']%1000,'linktitle':p['linktitle'],'id':p['id']}
			send_list.append(rec)
		mc.set('TRENDING_LIST_QUERY',send_list,1800)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Trending','PageDesc':'Today\'s hottest articles','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)	

def top3hr(request):
	DAY, MONTH, YEAR, HOUR,expiretime = fnReturnTimes()
	mcHour=mc.get('trendingHour')
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	print FQUERY
	LATEST_NEWS_LIST=latestnews()
	title=''
	send_list=mc.get('THREEHOUR_LIST_QUERY')
	tw_timeline=GetTimeline() 
	if send_list:
		pass
	else:	
		send_list=[]	
		THREEHOUR_LIST_QUERY=db.threehour.find().sort('place',1)
		for p in THREEHOUR_LIST_QUERY:
			rec={'title':p['title'],'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id']}
			send_list.append(rec)
		mc.set('THREEHOUR_LIST_QUERY',send_list,1800)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Top','PageDesc':'A three hour rolling average showing the most puopular articles currently','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)


def cold(request):
	DAY, MONTH, YEAR, HOUR,expiretime = fnReturnTimes()
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	COLD_LIST_QUERY=db.prodcold.find().sort('delta',1).limit(50)
	LATEST_NEWS_LIST=latestnews()
	tw_timeline=GetTimeline() 
 	send_list=[]
	title=''
	for p in COLD_LIST_QUERY:
		rec={'title':p['title'],'place':p['place'],'Hits':p['Hits'],'linktitle':p['linktitle'],'id':p['id']}
		send_list.append(rec)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Cooling','PageDesc':'The pages with the biggest drop in standings from yesterday to today.','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)


def randPage(request):
	TODAY=date.today()
	YEAR=TODAY.year
	DAY=TODAY.day
	MONTH=TODAY.month
	now=datetime.datetime.now()
	half=now+datetime.timedelta(minutes=45)
	stamp=mktime(half.timetuple())
	expiretime=format_date_time(stamp)
	DAY-=1
	if DAY==0:
	   DAY=30
	   MONTH-=1
	if MONTH==0:
	   DAY=31
	   MONTH=12
	   YEAR-=1
	t=get_template('RedTieIndex.html')
 	send_list=[]
	title=''
	utitle='<unknown>'
	send_list=mc.get('RANDOM_ARTICLES')
	tw_timeline=GetTimeline() 
        if send_list:
                pass
        else:

		for a in range(1,50):
			place=random.randint(1,250000)
			FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR),'place':place}
			RANDOM_LIST_QUERY=db.tophits.find(FQUERY)
			for item in RANDOM_LIST_QUERY:
				id=item['id']
				QUERY={'_id':id}
				NAMEQ=db.map.find(QUERY)
				for b in NAMEQ:
					title=b['title']
					s_title=string.replace(title,'_',' ')
	    		                t_title=s_title.encode('utf-8')
	       	               		utitle=urllib2.unquote(t_title)
			rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':title.encode('utf-8'),'id':item['id']}
			send_list.append(rec)
	mc.set('RANDOM_ARTICLES',send_list,60*60)
	LATEST_NEWS_LIST=db.news.find().sort('date',-1).limit(5)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Random','PageDesc':'A random sampling from a quarter million of Wikipedia\'s most popular pages! Refreshes about every 20 minutes.','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)


def debuts(request):
	TODAY=date.today()
	DAY=TODAY.day
	MONTH=TODAY.month
	YEAR=TODAY.year
	now=datetime.datetime.now()
	half=now+datetime.timedelta(minutes=45)
	stamp=mktime(half.timetuple())
	expiretime=format_date_time(stamp)
	t=get_template('RedTieIndex.html')
	QUERY=db.proddebuts.find({'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}).limit(100)
	RECPERTABSET=50
	LATEST_NEWS_LIST=db.news.find().sort('date',-1).limit(5)
        TOTALNEW=0
	send_list=mc.get('DEBUTS_ARTICLES')
	tw_timeline=GetTimeline() 
	if send_list:
		pass
	else:
		send_list=[]
	        for item in QUERY:
	                COUNT=0
	                TITLE=''
			title, utitle = MapQuery_FindName(item['id'])
			rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':item['linktitle'],'id':item['id']}
			send_list.append(rec)
	mc.set('DEBUTS_ARTICLES',send_list,60*60)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'Wikipedia\'s Debuting Pages','PageDesc':'Articles that have debuted in the most viewed list today','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)




