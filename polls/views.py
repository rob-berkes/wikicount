from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.cache import cache_page
from pymongo import Connection
from datetime import date
from lib import wikilib
import urllib2
import string
import random
import datetime
import hashlib
import redis
from wsgiref.handlers import format_date_time
from time import mktime
import time
import syslog
import subprocess
import os
import calendar
import HTMLParser
from django.shortcuts import render_to_response 
from django.template import RequestContext

_htmlparser=HTMLParser.HTMLParser()
unescape=_htmlparser.unescape

conn=Connection(wikilib.MONGO_IP)
db=conn.wc
RECORDSPERPAGE=50

#All purpose Functions

def getSiteName(LANG):
	if '.q' in LANG:
		SITENAME='wikiquote'
	elif '.b' in LANG:
		SITENAME='wikibooks'
	elif '.d' in LANG:
		SITENAME='wiktionary'
	elif '.m' in LANG:
		SITENAME='wikimedia'
	else:
		SITENAME='wikipedia'
	return SITENAME

def ReturnHexDigest(article):
	hd=hashlib.sha1(article).hexdigest()
	return hd

def fnReturnTitleI18(id,LANG='en'):
	hmCOLL=str(LANG)+"_hitsmap"
	RESULT=db[hmCOLL].find_one({'_id':id})

	try:
		return RESULT['title']
	except TypeError:
		return 'err:Name not found'


def GetTimeline():
	status=db.twitter.find()
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



DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()




def fnReturnStringDate(DAY,MONTH,YEAR):
	DAY='%02d' % (DAY,)	
	MONTH='%02d' % (MONTH,)	
	RETSTR=str(YEAR)+"_"+str(MONTH)+"_"+str(DAY)
	return RETSTR

def GenArchiveListI18(LANG='en'):
	PLACECOLL=str(LANG)+"_mapPlace"
	thCOLL=str(LANG)+"_tophits"
	archive_list=[]
	m12=False
	m1=False
	m2=False
	m3=False
	m4=False
	m5=False
	m6=False
	m7=False
	m8=False
	m9=False
	m10=False
	m11=False
	dec12={'text':'Dec 2012','d': '31','m':'12','y':'2012'}
	for a in range(1,32):
		CNAME=fnReturnStringDate(a,12,2012)
		if db[CNAME].count() > 1:
			archive_list.append(dec12)
			break
		jan13={'text':'Jan 2013','d': '28','m':'1','y':'2013','lang':LANG}
		feb13={'text':'Feb 2013','d': '28','m':'2','y':'2013','lang':LANG}
		mar13={'text':'Mar 2013','d': '28','m':'3','y':'2013','lang':LANG}
		apr13={'text':'Apr 2013','d': '28','m':'4','y':'2013','lang':LANG}
		may13={'text':'May 2013','d': '28','m':'5','y':'2013','lang':LANG}
		jun13={'text':'Jun 2013','d': '30','m':'6','y':'2013','lang':LANG}
		jul13={'text':'Jul 2013','d': '31','m':'7','y':'2013','lang':LANG}
		aug13={'text':'Aug 2013','d': '31','m':'8','y':'2013','lang':LANG}
		sept13={'text':'Sept 2013','d': '30','m':'9','y':'2013','lang':LANG}
		oct13={'text':'Oct 2013','d': '31','m':'10','y':'2013','lang':LANG}
		nov13={'text':'Nov 2013','d': '31','m':'11','y':'2013','lang':LANG}
		dec13={'text':'Dec 2013','d': '31','m':'12','y':'2013','lang':LANG}
		
	for a in range(1,32):
		CNAME=fnReturnStringDate(a,1,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m1:
		m1=True
		archive_list.append(jan13)
		CNAME=fnReturnStringDate(a,2,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m2:
		m2=True
		archive_list.append(feb13)
		CNAME=fnReturnStringDate(a,3,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m3:
		m3=True
		archive_list.append(mar13)
		CNAME=fnReturnStringDate(a,4,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m4:
		m4=True
		archive_list.append(apr13)
		CNAME=fnReturnStringDate(a,5,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m5:
		m5=True
		archive_list.append(may13)
		CNAME=fnReturnStringDate(a,6,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m6:
		m6=True
		archive_list.append(jun13)
		CNAME=fnReturnStringDate(a,7,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m7:
		m7=True
		archive_list.append(jul13)
		CNAME=fnReturnStringDate(a,8,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m8:
		m8=True
		archive_list.append(aug13)
		CNAME=fnReturnStringDate(a,9,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m9:
		m9=True
		archive_list.append(sept13)
		CNAME=fnReturnStringDate(a,10,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m10:
		m10=True
		archive_list.append(oct13)
		CNAME=fnReturnStringDate(a,11,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m11:
		m11=True
		archive_list.append(nov13)
		CNAME=fnReturnStringDate(a,12,2013)
	if db[PLACECOLL].find({CNAME:{"$gt":0}}).count() > 1 and not m12:
		m12=True
		archive_list.append(dec13)
	return archive_list

def returnHourString(hour):
        HOUR='%02d' % (hour,)
	return HOUR


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
	tw_timeline=GetTimeline()
	t=get_template('IndexListLast.html')
	latest_news_list=wikilib.fnLatestnews()
	send_list=[]
	send_list=mc.get('HOURKEY')
	c=Context({'latest_hits_list':send_list,'latest_news_list':latest_news_list,'MONTHNAME':MONTHNAME,'y':YEAR,'m':MONTH,'d':DAY,'tw_timeline':tw_timeline,'latest_news_list':latest_news_list})
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
	hd=ReturnHexDigest(stitle)
	title,utitle=wikilib.fnFindName(hd)
	t=get_template('IndexSearchResults.html')
	MAPQ={'_id': str(hd)}
	MAPQUERY=db.hitsdaily.find(MAPQ).limit(20)
	send_list=[]
	infoview(request,hd)
	for item in MAPQUERY:
		rec={'id':str(item['_id']),'title':str(item['title']),'linktitle':utitle,'Hits':0}
		syslog.syslog("wikitrends-searchResults-Search for "+str(rec))
		send_list.append(rec)
	c=Context({'news_list':send_list,'expiretime':expiretime})
	rendered=t.render(c)
	return HttpResponse(rendered)


def searchForm(request):
	t=get_template('IndexSearch.html')
	send_list=[]
	c=Context({expiretime:expiretime})
	rendered=t.render(c)
	return HttpResponse(rendered)


def blog(request):
	BLOGQUERY=db.blog.find().sort('date',-1).limit(10)
	t=get_template('IndexBlog.html')
	send_list=[]
	title=''
	for p in BLOGQUERY:
		rec={'newsdate':p['date'],'headtext':p['text']}
		syslog.syslog("blog fn: "+str(rec))
		send_list.append(rec)
	c=Context({'news_list':send_list,expiretime:expiretime})
	rendered=t.render(c)
	return HttpResponse(rendered)


def dailypageI18(request,LANG='en',YEAR=2013,MONTH=7):
	syslog.syslog('dailypageI18: Req made, lang :'+str(LANG)+' Y: '+str(YEAR)+' M: '+str(MONTH))
	t=get_template('IndexDailyI18.html')
	MEMCACHEDAYLIST=str(LANG)+"_mcdpDaysList"+str(MONTH)+str(YEAR)
	send_list=mc.get(MEMCACHEDAYLIST)
	archive_list=GenArchiveListI18(LANG)
	if send_list==None:
		send_list=[]
	for a in range(1,31):
		COLLNAME=str(LANG)+"_mapPlace"
		DAYKEY=fnReturnStringDate(a,int(MONTH),YEAR)
		RESULTSET=db[COLLNAME].find({DAYKEY:{"$gt":1}}).count()
		if RESULTSET>0:
			rec={'d':a,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(a)}
			send_list.append(rec)
	mc.set(MEMCACHEDAYLIST,send_list,60*60*24)

	title=''
	c=Context({'news_list':send_list,expiretime:expiretime,'archive_list':archive_list,'LANGUAGE':LANG})
	rendered=t.render(c)
	return HttpResponse(rendered)

def listtopI18(request,LANG,YEAR,MONTH,DAY):
	MONTHNAME=fnCaseMonthName(int(MONTH))
	if str(LANG).endswith('.b'):
		t=get_template('IndexTopListBooksI18.html')
	else:
		t=get_template('IndexTopListI18.html')
	send_list=[]
	RETSTR=fnReturnStringDate(int(DAY),int(MONTH),YEAR)
	DAYKEY=str(LANG)+'_mapPlace'
	HITSKEY=str(LANG)+'_mapHits'
	syslog.syslog('wikilib-views.py-listtop DAYKEY='+DAYKEY)
	send_list=mc.get(DAYKEY)
	tw_timeline=GetTimeline()
	latest_news_list=wikilib.fnLatestnews()
	if send_list==None:
		send_list=[]
		RESULTSET=db[HITSKEY].find().sort(RETSTR,-1).limit(100)
	PLACE=1
	for row in RESULTSET:
		title=''
		utitle=''
	try:
		ATITLE=fnReturnTitleI18(row['_id'],LANG)
		title, utitle=wikilib.fnFormatName(ATITLE)
	except KeyError:
		pass
	HITS=db[HITSKEY].find_one({'_id':row['_id']})
	try:
		rec={'place':PLACE,'Hits':HITS[RETSTR],'title':utitle ,'id':str(row['_id']),'linktitle':title.encode('utf-8'),'LANG':LANG,'LANGSUB':LANG[0:2]}
		send_list.append(rec)
	except KeyError:
		pass
	PLACE+=1
	mc.set('DAYKEY',send_list,7200)
	LANGSTR=wikilib.fnReturnLanguageName(LANG)
	PageTitle='Top Articles for '+str(LANGSTR)+' Wikipedia on '+str(YEAR)+'/'+str(MONTH)+'/'+str(DAY)+'.'
	c=Context({'PageTitle':PageTitle,'latest_hits_list':send_list,'y':YEAR,'m':MONTH,'d':DAY,'tw_timeline':tw_timeline,'latest_news_list':latest_news_list,'LANGUAGE':LANG})
	rendered=t.render(c)
	return HttpResponse(rendered)

def debug(request):
	t=get_template('IndexDebug.html')
	newCal=calendar.HTMLCalendar(2013)
	newCalendar=newCal.formatyear(2013,3)
	SEARCHID=0
	PageDesc=''
	sendlist=''
	c=Context({'Calendar':newCalendar,'ArticleTitle':'1169 Sicily Earthquake','ArticleHash':SEARCHID,'PageDesc':PageDesc,'send_list':sendlist})
	rendered=t.render(c)
	return HttpResponse(rendered)

def Mobile_Hourly(request,LANG,id):

	t=get_template('MobileHourly.htm')
	title,utitle=wikilib.fnFindName(LANG,id)
	
	c=Context({'expiretime':expiretime,'PageTitle':utitle,'linktitle':title,'HOURGRAPHFILENAME':str(id),'LANG':str(LANG)})
	rendered=t.render(c)

	return HttpResponse(rendered)

def returnSimilars(LANG,id):
	LLIST=[]
	SD=str(LANG)+'_similarity'
	RES=db[SD].find_one({'_id':id})
	try:
# for item in RES['similars']:
# rec={'id':item['id'],'title':item['title'],'score':item['score']}
# LLIST.append(rec)
		LLIST=RES['similars']
	except:
		pass
	return LLIST

def Mobile_infoviewI18(request,LANG,id):
	tw_timeline=GetTimeline()
	SLIST=returnSimilars(LANG,id)
	t=get_template('MobileInfoviewIndex.htm')
	title,utitle=wikilib.fnFindName(LANG,id)
	HOURGRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/hourly/'
	DAILYGRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/daily/'
	T25GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t25/'
        T50GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t50/'
	T100GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t100/'
	T500GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t500/'
	T1KGRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t1k/'

	HOURLYGRAPHFILENAME=str(id)
	DAILYGRAPHFILENAME=DAILYGRAPHDIRECTORY+str(id)+'.png'
	T25GRAPHFILENAME=T25GRAPHDIRECTORY+str(id)+'.png'
	T50GRAPHFILENAME=T50GRAPHDIRECTORY+str(id)+'.png'
	T100GRAPHFILENAME=T100GRAPHDIRECTORY+str(id)+'.png'
	T500GRAPHFILENAME=T500GRAPHDIRECTORY+str(id)+'.png'
	T1KGRAPHFILENAME=T1KGRAPHDIRECTORY+str(id)+'.png'
	

	try:
		T25GRAPHFILESIZE=os.path.getsize(T25GRAPHFILENAME)
	except OSError:
		T25GRAPHFILESIZE=0

	try:
		T50GRAPHFILESIZE=os.path.getsize(T50GRAPHFILENAME)
	except OSError:
		T50GRAPHFILESIZE=0

	try:
		T100GRAPHFILESIZE=os.path.getsize(T100GRAPHFILENAME)
	except OSError:
		T100GRAPHFILESIZE=0

	try:
		T500GRAPHFILESIZE=os.path.getsize(T500GRAPHFILENAME)
	except OSError:
		T500GRAPHFILESIZE=0

	try:
		T1KGRAPHFILESIZE=os.path.getsize(T1KGRAPHFILENAME)
	except OSError:
		T1KGRAPHFILESIZE=0

	SITENAME=getSiteName(LANG)
	c=Context({'PageDesc':'','PageTitle':utitle,'expiretime':expiretime,'linktitle':title,'tw_timeline':tw_timeline,'DAILYGRAPHFILENAME':DAILYGRAPHFILENAME,'HOURGRAPHFILENAME':HOURLYGRAPHFILENAME,'T25GRAPHFILENAME':T25GRAPHFILENAME,'T50GRAPHFILENAME':T50GRAPHFILENAME,'T100GRAPHFILENAME':T100GRAPHFILENAME,'T500GRAPHFILENAME':T500GRAPHFILENAME,'T1KGRAPHFILENAME':T1KGRAPHFILENAME,'LANG':str(LANG),'SITENAME':SITENAME,'ID':id,'SLIST':SLIST})
	rendered=t.render(c)

	return HttpResponse(rendered)

def infoviewI18(request,LANG,id):
    latest_news_list=wikilib.fnLatestnews()
    tw_timeline=GetTimeline()
    SLIST=returnSimilars(LANG,id)
    t=get_template('InfoviewIndex.htm')
    title,utitle=wikilib.fnFindName(LANG,id)
    HOURGRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/hourly/'
    DAILYGRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/daily/'
    T25GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t25/'
    T50GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t50/'
    T100GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t100/'
	T500GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t500/'
	T1KGRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t1k/'

	HOURLYGRAPHFILENAME=HOURGRAPHDIRECTORY+str(id)+'.png'
	DAILYGRAPHFILENAME=DAILYGRAPHDIRECTORY+str(id)+'.png'
	T25GRAPHFILENAME=T25GRAPHDIRECTORY+str(id)+'.png'
	T50GRAPHFILENAME=T50GRAPHDIRECTORY+str(id)+'.png'
	T100GRAPHFILENAME=T100GRAPHDIRECTORY+str(id)+'.png'
	T500GRAPHFILENAME=T500GRAPHDIRECTORY+str(id)+'.png'
	T1KGRAPHFILENAME=T1KGRAPHDIRECTORY+str(id)+'.png'


	try:
		T25GRAPHFILESIZE=os.path.getsize(T25GRAPHFILENAME)
	except OSError:
		T25GRAPHFILESIZE=0

	try:
		T50GRAPHFILESIZE=os.path.getsize(T50GRAPHFILENAME)
	except OSError:
		T50GRAPHFILESIZE=0

	try:
		T100GRAPHFILESIZE=os.path.getsize(T100GRAPHFILENAME)
	except OSError:
		T100GRAPHFILESIZE=0

	try:
		T500GRAPHFILESIZE=os.path.getsize(T500GRAPHFILENAME)
    except OSError:
		T500GRAPHFILESIZE=0

try:
    T1KGRAPHFILESIZE=os.path.getsize(T1KGRAPHFILENAME)
except OSError:
    T1KGRAPHFILESIZE=0

	c=Context({'PageDesc':'Click above to go the Wikipedia page.','latest_news_list':latest_news_list,'PageTitle':utitle,'expiretime':expiretime,'linktitle':title,'tw_timeline':tw_timeline,'DAILYGRAPHFILENAME':DAILYGRAPHFILENAME,'HOURGRAPHFILENAME':HOURLYGRAPHFILENAME,'T25GRAPHFILENAME':T25GRAPHFILENAME,'T50GRAPHFILENAME':T50GRAPHFILENAME,'T100GRAPHFILENAME':T100GRAPHFILENAME,'T500GRAPHFILENAME':T500GRAPHFILENAME,'T1KGRAPHFILENAME':T1KGRAPHFILENAME,'LANG':str(LANG),'ID':id,'SLIST':SLIST})
	rendered=t.render(c)

	return HttpResponse(rendered)



def category_trending(request):
	mcHour=mc.get('trendingHour')
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	LATEST_NEWS_LIST=wikilib.fnLatestnews()
	title=''
	send_list=mc.get('CATEGORY_TRENDING_LIST_QUERY')
	tw_timeline=GetTimeline()
	DAYKEY=fnReturnStringDate(DAY,MONTH,YEAR)
	send_list=[]	
	CATEGORY_TRENDING_LIST_QUERY=db.categorydaily.find().sort(DAYKEY,-1).limit(100)
	COUNT=0
	for p in CATEGORY_TRENDING_LIST_QUERY:
		COUNT+=1
		r=db.category.find_one({"_id":p["_id"]})
		rec={'title':r['title'],'place':COUNT,'Hits':p[DAYKEY],'linktitle':r['title'],'id':p['_id']}
		send_list.append(rec)
	mc.set('CATEGORY_TRENDING_LIST_QUERY',send_list,1800)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'Wikipedia\'s most popular categories','PageDesc':'Today\'s hottest categories','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)	

def file_trending(request):
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	LATEST_NEWS_LIST=wikilib.fnLatestnews()
	title=''
	tw_timeline=GetTimeline()
	DAYKEY=fnReturnStringDate(DAY,MONTH,YEAR)
	send_list=[]	
	FILE_TRENDING_LIST_QUERY=db.prodimagetrend.find().sort('Hits',-1).limit(100)
	for p in FILE_TRENDING_LIST_QUERY:
		rec={'title':p['title'],'place':p['place'],'Hits':p['Hits'],'linktitle':p['linktitle'],'id':p['id']}
		send_list.append(rec)
	mc.set('FILE_TRENDING_LIST_QUERY',send_list,1800)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Trending Files/Images','PageDesc':'The most popular image files of the day','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)	

def MobileLanguageList(request,LANG='en'):
	t=get_template('MobileLangList.html')
	LANGLIST=wikilib.getLanguageList()
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
	PAGEDATE=str(MONTHNAME)+" "+str(DAY)+" "+str(YEAR)
	send_list=[]
	for lang in LANGLIST:
		PAGETITLE=str(wikilib.fnReturnLanguageName(lang))
		record={'LANG':str(lang),'title':PAGETITLE}
		send_list.append(record)
	PAGETITLE="Languages"
	c=Context({'PageDate':PAGEDATE,'PageTitle':PAGETITLE,'expiretime':expiretime,'language_list':send_list})
	rendered=t.render(c)
	return HttpResponse(rendered)

def mobileIndexLang(request,LANG='en'):
	RangeList=wikilib.fnRangeCount(5)
	DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
	request.encoding='iso-8859-1'
	MONTHNAME=fnCaseMonthName(MONTH)
	t=get_template('MobileIndexI18.html')
	title=''
	archive_list=GenArchiveListI18(LANG)
	PLACE=1
	REDIS_ID_KEY=str(LANG)+'_'+str(PLACE)+'_'+'ID'
	rc=redis.Redis('localhost')
	mcVAR=str(LANG)+"_THREEHOUR"
	SITENAME=getSiteName(LANG)
	LANGSUB=LANG[0:2]
	send_list=[]	
	try:
		aTITLE=str(rc.get(REDIS_ID_KEY))
		artID=aTITLE
	except:
		aTITLE='None'
		if aTITLE=='None' or aTITLE=='':
			COLLNAME=str(LANG)+"_threehour"
			THREEHOUR_LIST_QUERY=db[COLLNAME].find().sort('place',1)
		if str(LANG)=='commons.m':
			LANGSUB='commons'
			for p in THREEHOUR_LIST_QUERY:
				tstr=str(p['title'])
				rec={'title':urllib2.unquote(tstr),'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id'],'LANG':LANG,'LANGSUB':LANGSUB,'SITENAME':SITENAME}
				send_list.append(rec)
				PLACE+=1
		else:
			rc.set(REDIS_ID_KEY,str(aTITLE))
			send_list=[]
			PLACE=1
			while artID!="None" and artID!='' and PLACE<100:
				REDIS_TITLE_KEY=str(LANG)+'_'+str(artID)+'_'+'TITLE'
				REDIS_AVG_KEY=str(LANG)+'_'+str(artID)+'_'+'AVG'
				REDIS_LINKTITLE_KEY=str(LANG)+'_'+str(artID)+'_'+'LINKTITLE'
				aaTITLE=rc.get(REDIS_TITLE_KEY)
				aAVG=rc.get(REDIS_AVG_KEY)
				aLINKTITLE=rc.get(REDIS_LINKTITLE_KEY)
				aID=rc.get(REDIS_ID_KEY)
				tstr=str(aaTITLE)
				SITENAME=getSitename(LANG)
				LANGSUB=LANG[0:2]
				if 'commons' in LANG:
					LANGSUB='commons'
					rec={'LANGSUB':LANGSUB,'SITENAME':SITENAME,'title':urllib2.unquote(tstr),'place':PLACE,'Avg':aAVG,'linktitle':aLINKTITLE,'id':aID,'LANG':str(LANG)}
					send_list.append(rec)
				PLACE+=1
				REDIS_ID_KEY=str(LANG)+'_'+str(PLACE)+'_ID'
				artID=rc.get(REDIS_ID_KEY)
				PAGETITLE=str(wikilib.fnReturnLanguageName(LANG))
				PAGEDATE=str(MONTHNAME)+" "+str(DAY)+" "+str(YEAR)
	c=Context({'PageDate':PAGEDATE,'RangeList':RangeList,'latest_hits_list':send_list,'PageTitle':PAGETITLE,'expiretime':expiretime,'archive_list':archive_list,'LANGUAGE':LANG})
	rendered=t.render(c)
	return HttpResponse(rendered)


def spam(request,id):
	try:
		db['spam'].insert({'_id':id})
	except:
		pass
	return indexLang(request)

def indexTopix(request,LANG='en'):
    DAY,MONTH, YEAR, HOUR, expiretime, MONTHNAME = fnReturnTimes()
    request.encoding = 'iso-8859-1'
    MONTHNAME=fnCaseMonthName(MONTH)
    if str(LANG).endswith('.b'):
        t=get_template('RedTieIndexBooksI18.html')
    elif str(LANG).endswith('.s'):
        t=get_template('RedTieIndexSourceI18.html')
    elif str(LANG).endswith('.q'):
        t=get_template('RedTieIndexQuoteI18.html')
    elif str(LANG).endswith('.d'):
        t=get_template('RedTieIndexDictI18.html')
    elif str(LANG).endswith('.voy'):
        t=get_template('RedTieIndexVoyI18.html')
    elif str(LANG)=='commons':
        t=get_template('RedTieIndexComI18.html')
        LANG='commons.m'
    else:
        t=get_template('RedTieIndexI18.html')
    LATEST_NEWS_LIST=wikilib.fnLatestnews()
    title=''
    tw_timeline=GetTimeline()
    archive_list=GenArchiveListI18(LANG)
    PLACE=1
    REDIS_ID_KEY=str(LANG)+'_'+str(PLACE)+'_'+'ID'
    mcVAR=str(LANG)+"_THREEHOUR"
    rc=redis.Redis('localhost')
    send_list=[]
    try:
        aTITLE=str(rc.get(REDIS_ID_KEY))
        artID=aTITLE
    except:
        aTITLE='None'
    if aTITLE=='None' or aTITLE=='':
        COLLNAME=str(LANG)+"_threehour"
        THREEHOUR_LIST_QUERY=db[COLLNAME].find().sort('place',1)
        LANGSUB=LANG[0:2]
        if str(LANG)=='commons.m':
            LANGSUB='commons'
        for p in THREEHOUR_LIST_QUERY:
            tstr=str(p['title'])
            rec={'title':urllib2.unquote(tstr),'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id'],'LANG':LANG,'LANGSUB':LANGSUB}
            send_list.append(rec)
            PLACE+=1
    else:
        rc.set(REDIS_ID_KEY,str(aTITLE))
        send_list=[]
        PLACE=1
        while artID!="None" and artID!='' and PLACE<100:
            REDIS_TITLE_KEY=str(LANG)+'_'+str(artID)+'_'+'TITLE'
            REDIS_AVG_KEY=str(LANG)+'_'+str(artID)+'_'+'AVG'
            REDIS_LINKTITLE_KEY=str(LANG)+'_'+str(artID)+'_'+'LINKTITLE'
            aaTITLE=rc.get(REDIS_TITLE_KEY)
            aAVG=rc.get(REDIS_AVG_KEY)
            aLINKTITLE=rc.get(REDIS_LINKTITLE_KEY)
            aID=rc.get(REDIS_ID_KEY)
            tstr=str(aaTITLE)
            rec={'title':urllib2.unquote(tstr),'place':PLACE,'Avg':aAVG,'linktitle':aLINKTITLE,'id':aID,'LANG':str(LANG)}
            send_list.append(rec)
            rc.set(REDIS_TITLE_KEY,aaTITLE)
            rc.set(REDIS_AVG_KEY,aAVG)
            rc.set(REDIS_LINKTITLE_KEY,aLINKTITLE)
            rc.set(REDIS_ID_KEY,aID)
            PLACE+=1
            REDIS_ID_KEY=str(LANG)+'_'+str(PLACE)+'_ID'
            artID=rc.get(REDIS_ID_KEY)
    PAGETITLE="Top "+str(wikilib.fnReturnLanguageName(LANG))+" pages for "+str(MONTHNAME)+" "+str(DAY)+", "+str(YEAR)
    c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':PAGETITLE,'PageDesc':'Computes the three hour rolling average and find the most popular articles compared to yesterday!','expiretime':expiretime,'tw_timeline':tw_timeline,'archive_list':archive_list,'LANGUAGE':LANG})
    DATADICTIONARY = {'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':PAGETITLE,'PageDesc':'By three hour rolling average, find the most trending articles at this hour, compared to yesterday. Updated hourly around 20 past!','expiretime':expiretime,'tw_timeline':tw_timeline,'archive_list':archive_list,'LANGUAGE':LANG}
    return render_to_response('RedTieIndexI18OneCol.html',DATADICTIONARY,context_instance=RequestContext(request))


def indexLang(request,LANG='en'):
    DAY, MONTH, YEAR, HOUR,expiretime,MONTHNAME = fnReturnTimes()
    request.encoding='iso-8859-1'
    MONTHNAME=fnCaseMonthName(MONTH)
    if str(LANG).endswith('.b'):
        t=get_template('RedTieIndexBooksI18.html')
    elif str(LANG).endswith('.s'):
        t=get_template('RedTieIndexSourceI18.html')
    elif str(LANG).endswith('.q'):
        t=get_template('RedTieIndexQuoteI18.html')
    elif str(LANG).endswith('.d'):
        t=get_template('RedTieIndexDictI18.html')
    elif str(LANG).endswith('.voy'):
        t=get_template('RedTieIndexVoyI18.html')
    elif str(LANG)=='commons':
        t=get_template('RedTieIndexComI18.html')
        LANG='commons.m'
    else:
        t=get_template('RedTieIndexI18.html')
    LATEST_NEWS_LIST=wikilib.fnLatestnews()
    title=''
    tw_timeline=GetTimeline()
    archive_list=GenArchiveListI18(LANG)
    PLACE=1
    REDIS_ID_KEY=str(LANG)+'_'+str(PLACE)+'_'+'ID'
    mcVAR=str(LANG)+"_THREEHOUR"
    rc=redis.Redis('localhost')
    send_list=[]
    try:
        aTITLE=str(rc.get(REDIS_ID_KEY))
        artID=aTITLE
    except:
        aTITLE='None'
    if aTITLE=='None' or aTITLE=='':
        COLLNAME=str(LANG)+"_threehour"
        THREEHOUR_LIST_QUERY=db[COLLNAME].find().sort('place',1)
        LANGSUB=LANG[0:2]
        if str(LANG)=='commons.m':
            LANGSUB='commons'
        for p in THREEHOUR_LIST_QUERY:
            tstr=str(p['title'])
            rec={'title':urllib2.unquote(tstr),'place':p['place'],'Avg':p['rollavg'],'linktitle':p['title'],'id':p['id'],'LANG':LANG,'LANGSUB':LANGSUB}
            send_list.append(rec)
            PLACE+=1
    else:
        rc.set(REDIS_ID_KEY,str(aTITLE))
        send_list=[]
        PLACE=1
        while artID!="None" and artID!='' and PLACE<100:
            REDIS_TITLE_KEY=str(LANG)+'_'+str(artID)+'_'+'TITLE'
            REDIS_AVG_KEY=str(LANG)+'_'+str(artID)+'_'+'AVG'
            REDIS_LINKTITLE_KEY=str(LANG)+'_'+str(artID)+'_'+'LINKTITLE'
            aaTITLE=rc.get(REDIS_TITLE_KEY)
            aAVG=rc.get(REDIS_AVG_KEY)
            aLINKTITLE=rc.get(REDIS_LINKTITLE_KEY)
            aID=rc.get(REDIS_ID_KEY)
            tstr=str(aaTITLE)
            rec={'title':urllib2.unquote(tstr),'place':PLACE,'Avg':aAVG,'linktitle':aLINKTITLE,'id':aID,'LANG':str(LANG)}
            send_list.append(rec)
            rc.set(REDIS_TITLE_KEY,aaTITLE)
            rc.set(REDIS_AVG_KEY,aAVG)
            rc.set(REDIS_LINKTITLE_KEY,aLINKTITLE)
            rc.set(REDIS_ID_KEY,aID)
            PLACE+=1
            REDIS_ID_KEY=str(LANG)+'_'+str(PLACE)+'_ID'
            artID=rc.get(REDIS_ID_KEY)
    PAGETITLE="Top "+str(wikilib.fnReturnLanguageName(LANG))+" pages for "+str(MONTHNAME)+" "+str(DAY)+", "+str(YEAR)
    c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':PAGETITLE,'PageDesc':'Computes the three hour rolling average and find the most popular articles compared to yesterday!','expiretime':expiretime,'tw_timeline':tw_timeline,'archive_list':archive_list,'LANGUAGE':LANG})
    DATADICTIONARY = {'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':PAGETITLE,'PageDesc':'By three hour rolling average, find the most trending articles at this hour, compared to yesterday. Updated hourly around 20 past!','expiretime':expiretime,'tw_timeline':tw_timeline,'archive_list':archive_list,'LANGUAGE':LANG}

    #	rendered=t.render(c)
    #	return HttpResponse(rendered)
    return render_to_response('RedTieIndexI18.html',DATADICTIONARY,context_instance=RequestContext(request))

def cold(request):
	t=get_template('RedTieIndex.html')
	FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR)}
	COLD_LIST_QUERY=mc.get('COLD_LIST_QUERY')
	LATEST_NEWS_LIST=wikilib.fnLatestnews()
	tw_timeline=GetTimeline()
	send_list=[]
	title=''
	c=Context({'latest_hits_list':COLD_LIST_QUERY,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Cooling','PageDesc':'The pages with the biggest drop in standings from yesterday to today.','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)


def randPage(request):
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
	if send_list==None:
		for a in range(1,50):
			place=random.randint(1,250000)
			FQUERY={'d':int(DAY),'m':int(MONTH),'y':int(YEAR),'place':place}
			RANDOM_LIST_QUERY=db['tophits'+str(YEAR)+MONTHNAME].find(FQUERY)
			for item in RANDOM_LIST_QUERY:
				title, utitle=wikilib.fnFormatName(item['title'])
				rec={'title':utitle,'place':item['place'],'Hits':item['Hits'],'linktitle':title.encode('utf-8'),'id':item['id']}
				send_list.append(rec)
				mc.set('RANDOM_ARTICLES',send_list,60*60)
	LATEST_NEWS_LIST=db.news.find().sort('date',-1).limit(5)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'WikiTrends.Info - Random','PageDesc':'A random sampling from a quarter million of Wikipedia\'s most popular pages! Refreshes about every 20 minutes.','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)


def debuts(request):
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
	mc.set('DEBUTS_ARTICLES',send_list,60*60)
	c=Context({'latest_hits_list':send_list,'latest_news_list':LATEST_NEWS_LIST,'PageTitle':'Wikipedia\'s Debuting Pages','PageDesc':'Articles that have debuted in the most viewed list today','expiretime':expiretime,'tw_timeline':tw_timeline})
	rendered=t.render(c)
	return HttpResponse(rendered)
