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
import os

conn=Connection('10.115.126.7')
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
def MapQuery_FindCategory(id):
	QUERY={'id':id}
        MAPQ=db.category.find({'_id':id})
        latest_news_list = latestnews()
	title=''
	utitle=''
        for name in MAPQ:
                        title=name['title']
                        s_title=string.replace(title,'_',' ')
                        t_title=s_title.encode('utf-8')
                        utitle=urllib2.unquote(t_title)


	return title, utitle
def MapQuery_FindImage(id):
	QUERY={'id':id}
        MAPQ=db.image.find({'_id':id})
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
	MONTHNAME=datetime.datetime.now().strftime("%B")
	return DAY, MONTH, YEAR,HOUR, expiretime,MONTHNAME
def fnReturnStringDate(DAY,MONTH,YEAR):
	DAY='%02d' % (DAY,)	
	MONTH='%02d' % (MONTH,)	
	RETSTR=str(YEAR)+"_"+str(MONTH)+"_"+str(DAY)
	return RETSTR

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

def fnCaseMonthName(MONTH):
	if MONTH==1:
		return 'January'
	elif MONTH==2:
		return 'February'
	elif MONTH==3:
		return 'March'
	elif MONTH==4:
		return 'April'
	elif MONTH==5:
		return 'May'
	elif MONTH==6:
		return 'June'
	elif MONTH==7:
		return 'July'
	elif MONTH==8:
		return 'August'
	elif MONTH==9:
		return 'September'
	elif MONTH==10:
		return 'October'
	elif MONTH==11:
		return 'November'
	elif MONTH==12:
		return 'December'
	else:
		return 'Unknown'



#Begin application functions

def listLastHour(request):
	DAY,MONTH,YEAR,HOUR,expiretime,MONTHNAME=fnReturnTimes()
	tw_timeline=GetTimeline()
	t=get_template('IndexListLast.html')
	latest_news_list=latestnews()
	SEARCH_HOUR=adjustHourforLastHour(HOUR)
	SEARCH_HOUR='%02d' % (SEARCH_HOUR,)
	HOURQUERY=db.hitshourlydaily.find({str(SEARCH_HOUR):{'$gt':1}}).sort(str(SEARCH_HOUR),-1).limit(50)
	send_list=[]
	place=1
	HOURKEY="SEARCHHOUR_"+str(SEARCH_HOUR)
	send_list=mc.get(HOURKEY)
	if len(send_list)>0:
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
	MAPQUERY=db.hitsdaily.find(MAPQ).limit(20)
	send_list=[]
	infoview(request,hd)
	for item in MAPQUERY:
		rec={'id':str(item['_id']),'title':str(item['title']),'linktitle':utitle,'Hits':item['Hits']}
		syslog.syslog("wikitrends-searchResults-Search for "+str(rec))
		send_list.append(rec)
	c=Context({'news_list':send_list,'expiretime':expiretime})
	rendered=t.render(c)
	return HttpResponse(rendered)
	

def searchForm(request):
	DAY,MONTH,YEAR,HOUR,expiretime,MONTHNAME=fnReturnTimes()
	t=get_template('IndexSearch.html')
	send_list=[]
	c=Context({expiretime:expiretime})
	rendered=t.render(c)
	return HttpResponse(rendered)


def blog(request):
	DAY,MONTH,YEAR,HOUR,expiretime,MONTHNAME=fnReturnTimes()
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
	DAY,MONTH,YEAR,HOUR,expiretime,MONTHNAME=fnReturnTimes()
	syslog.syslog('wc-dailypage MONTH='+str(MONTH))
	junk1,junk2,junk3,junk4,expiretime=fnReturnTimes()
	t=get_template('IndexDaily.html')
	send_list=mc.get('mcdpDaysList'+str(MONTH)+str(YEAR))
	archive_list=GenArchiveList()
	if len(send_list)>0:
		pass
	else:
		send_list=[]
		RESULTSET=db.command({'distinct':'tophits'+str(YEAR)+MONTHNAME,'key':'d','query':{'m':int(MONTH),'y':int(YEAR)}})
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
	MONTHNAME=fnCaseMonthName(int(MONTH))
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
	if len(send_list)>0:
		pass
	else:
		send_list=[]
		RESULTSET=db['tophits'+str(YEAR)+MONTHNAME].find(QUERY).sort('place',1).limit(100)
		for row in RESULTSET:
			title=''
			utitle=''
			try:
				title, utitle=FormatName(row['title'])
			except KeyError:
				pass
			rec={'place':row['place'],'Hits':row['Hits'],'title':utitle ,'id':str(row['id']),'linktitle':title.encode('utf-8')}
			send_list.append(rec)
		mc.set('DAYKEY',send_list,7200)
	c=Context({'latest_hits_list':send_list,'y':YEAR,'m':MONTH,'d':DAY,'tw_timeline':tw_timeline,'latest_news_list':latest_news_list})
	rendered=t.render(c)
	return HttpResponse(rendered)


def debug(request):
	t=get_template('IndexHourly.html')
	c=Context({'ArticleTitle':'1169 Sicily Earthquake','ArticleHash':SEARCHID,'PageDesc':PageDesc,'send_list':sorted(HOUR_RS.iteritems())})
	rendered=t.render(c)
	return HttpResponse(rendered)


def infoview(request,id):
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()

        QUERY={'id':str(id)}
	print QUERY
	LTQUERY={'id':id,'place':{'$lt':50001}}
	LT5KQ={'id':id,'place':{'$lt':5001}}
	LT500Q={'id':id,'place':{'$lt':501}}
	LT50Q={'id':id,'place':{'$lt':51}}
	INFOVIEW_KEY='infoview_'+str(id)
	INFOVIEWLT_KEY='infoviewlt_'+str(id)
	INFOVIEWLT5K_KEY='infoviewlt5k_'+str(id)
	INFOVIEWLT500_KEY='infoviewlt500_'+str(id)
	INFOVIEWLT50_KEY='infoviewlt50_'+str(id)

	HOUR_RS=db.hitshourly.find_one({'_id':id})
	if HOUR_RS==None:
		HOUR_RS=db.categoryhourly.find_one({'_id':id})
	if HOUR_RS==None:
		HOUR_RS=db.imagehourly.find_one({'_id':id})
	latest_news_list = latestnews()
	
	tw_timeline=GetTimeline()
	send_list=[] 
	send_list=mc.get(INFOVIEW_KEY)
	info_lt50k_list=mc.get(INFOVIEWLT_KEY)
	info_lt5k_list=mc.get(INFOVIEWLT5K_KEY)	
	info_lt500_list=mc.get(INFOVIEWLT500_KEY)	
	info_lt50_list=mc.get(INFOVIEWLT50_KEY)	
	if send_list==None:
		send_list=[]
	if send_list==None:
		send_list=[]
		FINDQ=db['tophits'+str(YEAR)+MONTHNAME].find(QUERY).sort([('y',1),('m',1),('d',1)])
		DFINDQ=db.tophits.find(QUERY)
		for result in DFINDQ:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			send_list.append(rec)
		for result in FINDQ:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			send_list.append(rec)
		mc.set(INFOVIEW_KEY,send_list,60*60*24)
	if info_lt50k_list==None:
		info_lt50k_list=[]
        	LT50KQ=db['tophits'+str(YEAR)+MONTHNAME].find(LTQUERY)
		D50KFINDQ=db.tophits.find(LTQUERY)
		for result in D50KFINDQ:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			info_lt50k_list.append(rec)
		for result in LT50KQ:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			info_lt50k_list.append(rec)
		mc.set(INFOVIEWLT_KEY,info_lt50k_list,60*60*24)
	if info_lt500_list==None:
		info_lt500_list=[]
        	resLT500Q=db['tophits'+str(YEAR)+MONTHNAME].find(LT500Q)
		D500FINDQ=db.tophits.find(LT500Q)
		for result in D500FINDQ:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			info_lt500_list.append(rec)
		for res in resLT500Q:
			rec={'d':str(res['d']),'m':str(res['m']),'y':str(res['y']),'place':str(res['place'])}
			info_lt500_list.append(rec)
		mc.set(INFOVIEWLT500_KEY,info_lt500_list,60*60*24)
	if info_lt5k_list==None:
		info_lt5k_list=[]
        	resLT5KQ=db['tophits'+str(YEAR)+MONTHNAME].find(LT5KQ)
		D5KFINDQ=db.tophits.find(LT5KQ)
		for result in D5KFINDQ:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			info_lt5k_list.append(rec)
		for result in resLT5KQ:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			info_lt5k_list.append(rec)
		mc.set(INFOVIEWLT5K_KEY,info_lt5k_list,60*60*24)
	if info_lt50_list==None:
		info_lt50_list=[]
        	resLT50Q=db['tophits'+str(YEAR)+MONTHNAME].find(LT50Q)
		D50FINDQ=db.tophits.find(LT50Q)
		for result in D50FINDQ:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			info_lt50_list.append(rec)
		for result in resLT50Q:
			rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
			info_lt50_list.append(rec)
		mc.set(INFOVIEWLT50_KEY,info_lt50_list,60*60*24)


	title, utitle = MapQuery_FindName(id)
	if title=='':
		title,utitle = MapQuery_FindCategory(id)
	if title=='':
		title,utitle = MapQuery_FindImage(id)
	t=get_template('InfoviewIndex.htm')
	HOURGRAPHFILENAME='http://www.wikitrends.info/static/images/hourly/'+str(id)+'.png'
	T500GRAPHFILENAME='http://www.wikitrends.info/static/images/t500/'+str(id)+'.png'
	T5KGRAPHFILENAME='http://www.wikitrends.info/static/images/t5k/'+str(id)+'.png'
	T50KGRAPHFILENAME='http://www.wikitrends.info/static/images/t50k/'+str(id)+'.png'
	T250KGRAPHFILENAME='http://www.wikitrends.info/static/images/t250k/'+str(id)+'.png'
	T50GRAPHFILENAME='http://www.wikitrends.info/static/images/t50/'+str(id)+'.png'
	try:
		T50GRAPHFILESIZE=os.path.getsize(T50GRAPHFILENAME)
	except OSError:
		T50GRAPHFILESIZE=0
	try:
		T5KGRAPHFILESIZE=os.path.getsize(T5KGRAPHFILENAME)
	except OSError:
		T5KGRAPHFILESIZE=0
	try:
		T500GRAPHFILESIZE=os.path.getsize(T500GRAPHFILENAME)
	except OSError:
		T500GRAPHFILESIZE=0
	c=Context({'PageDesc':'Click above to go the Wikipedia page.','info_find_query':send_list,'latest_news_list':latest_news_list,'PageTitle':utitle,'expiretime':expiretime,'linktitle':title,'tw_timeline':tw_timeline,'hour_send_list':sorted(HOUR_RS.iteritems()),'info_lt50k_list':info_lt50k_list,'info_lt5k_list':info_lt5k_list,'info_lt500_list':info_lt500_list,'info_lt50_list':info_lt50_list,'HOURGRAPHFILENAME':HOURGRAPHFILENAME,'T500GRAPHFILENAME':T500GRAPHFILENAME,'T5KGRAPHFILENAME':T5KGRAPHFILENAME,'T50KGRAPHFILENAME':T50KGRAPHFILENAME,'T250KGRAPHFILENAME':T250KGRAPHFILENAME,'T50GRAPHFILENAME':T50GRAPHFILENAME,'T50GRAPHFILESIZE':T50GRAPHFILESIZE,'T5KGRAPHFILESIZE':T5KGRAPHFILESIZE,'T500GRAPHFILESIZE':T500GRAPHFILESIZE})
	rendered=t.render(c)
	return HttpResponse(rendered)


def trending(request):
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
	mcHour=mc.get('trendingHour')
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	print FQUERY
	LATEST_NEWS_LIST=latestnews()
	title=''
	send_list=mc.get('TRENDING_LIST_QUERY')
	tw_timeline=GetTimeline() 
	try:
		LENGTH_SEND=len(send_list)
	except TypeError:
		LENGTH_SEND=0
	if LENGTH_SEND > 0:
		pass
	else:	
		send_list=[]	
		TRENDING_LIST_QUERY=db.prodtrend.find().sort('Hits',-1).limit(100)
		for p in TRENDING_LIST_QUERY:
			rec={'title':p['title'],'place':p['place'],'Hits':p['Hits']%1000,'linktitle':p['linktitle'],'id':p['id']}
			send_list.append(rec)
		mc.set('TRENDING_LIST_QUERY',send_list,1800)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Trending','PageDesc':'Today\'s hottest articles','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)	

def category_trending(request):
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
	mcHour=mc.get('trendingHour')
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	LATEST_NEWS_LIST=latestnews()
	title=''
	send_list=mc.get('CATEGORY_TRENDING_LIST_QUERY')
	tw_timeline=GetTimeline()
	DAYKEY=str(YEAR)+"_"+str(MONTH)+"_"+str(DAY) 
	send_list=[]	
	CATEGORY_TRENDING_LIST_QUERY=db.prodcattrend.find().sort('Hits',-1).limit(100)
	for p in CATEGORY_TRENDING_LIST_QUERY:
		rec={'title':p['title'],'place':p['place'],'Hits':p['Hits'],'linktitle':p['linktitle'],'id':p['id']}
		send_list.append(rec)
	mc.set('CATEGORY_TRENDING_LIST_QUERY',send_list,1800)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Trending Categories','PageDesc':'Today\'s hottest categories','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)	
def file_trending(request):
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	LATEST_NEWS_LIST=latestnews()
	title=''
	tw_timeline=GetTimeline()
	DAYKEY=str(YEAR)+"_"+str(MONTH)+"_"+str(DAY) 
	send_list=[]	
	FILE_TRENDING_LIST_QUERY=db.prodimagetrend.find().sort('Hits',-1).limit(100)
	for p in FILE_TRENDING_LIST_QUERY:
		rec={'title':p['title'],'place':p['place'],'Hits':p['Hits'],'linktitle':p['linktitle'],'id':p['id']}
		send_list.append(rec)
	mc.set('FILE_TRENDING_LIST_QUERY',send_list,1800)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Trending Files/Images','PageDesc':'The most popular image files of the day','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)	

def imageMain(request):
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
	t=get_template('RedTieIndex.html')
	LATEST_NEWS_LIST=latestnews()
	title=''
	tw_timeline=GetTimeline() 
	send_list=[]	
	dateKey=str(YEAR)+"_"+str(MONTH)+"_"+str(DAY)
	TRENDING_LIST_QUERY=db.imagedaily.find({dateKey:{'$exists':True}}).sort(dateKey,-1).limit(100)
	for p in TRENDING_LIST_QUERY:
		print p
		rec={'title':p['title'],'Hits':p[datekey],'linktitle':p['title'],'id':p['_id']}
		send_list.append(rec)
#	mc.set('IMAGE_LIST_QUERY',send_list,1800)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'Wikipedias most popular Images','PageDesc':'Tracking direct links to images','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)	

def top3hr(request):
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
	mcHour=mc.get('trendingHour')
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	print FQUERY
	LATEST_NEWS_LIST=latestnews()
	title=''
	send_list=mc.get('THREEHOUR_LIST_QUERY')
	tw_timeline=GetTimeline() 
	if len(send_list)>0:
		pass
	else:	
		send_list=[]	
		THREEHOUR_LIST_QUERY=db.threehour.find().sort('place',1)
		for p in THREEHOUR_LIST_QUERY:
			rec={'title':p['title'],'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id']}
			send_list.append(rec)
		mc.set('THREEHOUR_LIST_QUERY',send_list,1800)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Top','PageDesc':'A three hour rolling average showing the most popular articles currently','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)


def cold(request):
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
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
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
	TODAY=date.today()
	now=datetime.datetime.now()
	half=now+datetime.timedelta(minutes=45)
	stamp=mktime(half.timetuple())
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
        if len(send_list)>0:
                pass
        else:

		for a in range(1,50):
			place=random.randint(1,250000)
			FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR),'place':place}
			RANDOM_LIST_QUERY=db['tophits'+str(YEAR)+MONTHNAME].find(FQUERY)
			for item in RANDOM_LIST_QUERY:
				title, utitle=FormatName(item['title'])
				rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':title.encode('utf-8'),'id':item['id']}
				send_list.append(rec)
	mc.set('RANDOM_ARTICLES',send_list,60*60)
	LATEST_NEWS_LIST=db.news.find().sort('date',-1).limit(5)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Random','PageDesc':'A random sampling from a quarter million of Wikipedia\'s most popular pages! Refreshes about every 20 minutes.','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)


def debuts(request):
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
	TODAY=date.today()
	now=datetime.datetime.now()
	half=now+datetime.timedelta(minutes=45)
	stamp=mktime(half.timetuple())
	t=get_template('RedTieIndex.html')
	QUERY=db['proddebuts'+str(YEAR)+MONTHNAME].find({'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}).sort('place',1).limit(300)
	LATEST_NEWS_LIST=db.news.find().sort('date',-1).limit(5)
        TOTALNEW=0
	send_list=mc.get('DEBUTS_ARTICLES')
	tw_timeline=GetTimeline() 
	if len(send_list)>0:
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




