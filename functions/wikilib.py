
import urllib2
import os
import string
import datetime 
from datetime import date
from pymongo import Connection 
import memcache
import time
import subprocess 
import syslog
import random

conn=Connection('10.164.95.114')
db=conn.wc

LLIST={ 'ru':'Russian Wikipedia',
	'en':'English Wikipedia',
	'ja':'Japanese Wikipedia',
	'zh':'Chinese Wikipedia',
	'es':'Spanish Wikipedia',
	'fr':'French Wikipedia',
	'pl':'Polish Wikipedia',
	'pt':'Portugese Wikipedia',
	'it':'Italian Wikipedia',
	'de':'German Wikipedia',
	'ro':'Romanian Wikipedia',
	'eo':'Esperanto Wikipedia',
	'hr':'Croatian Wikipedia',
	'ar':'Arabic Wikipedia',
	'la':'Latin Wikipedia',
	'sw':'Swahili Wikipedia',
	'simple':'SimpleEnglish Wikipedia',
	'af':'Afrikaans Wikipedia',
	'en.b':'English Wikibooks',
	'en.q':'English Wikiquote',
	'en.s':'English Wikisource',
	'en.d':'Wiktionary',
	'en.voy':'English Wikivoyage',
	'fr.d':'French Wiktionary',
	'fr.b':'French Wikibooks',
	'sv':'Svenska Wikipedia',
	'ja.b':'Japanese Wikibooks',
	'it.b':'Italian Wikibooks',
	'de.b':'German Wikibooks',
	'commons.m':'Wikimedia Commons',
	'it.q':'Italian Wikiquote',
	'pl.q':'Polish Wikiquote',
	'ru.q':'Russian Wikiquote',
	'zh.q':'Chinese Wikiquote',
	'zh.b':'Chinese Wikibook',
	'ru.b':'Russian Wikibook'}

def fnRangeCount(value):
	return [v+1 for v in range(0,value)]
def fnReturnLanguageName(LANG):
	return LLIST[LANG]
def getLanguageList():
	return LLIST.keys()
def fnDrawGraph(type,id,LANG):
	TESTNUM=random.randint(1,20)
	GRAPHDICT={'25':'t25',
                  '50':'t50',
                  '100':'t100',
                  '500':'t500',
                  '1000':t1k',
                  '365':'daily'}
	OUTFILENAME==('/tmp/django/wikicount/static/images/%s/%s/%s.png' % (LANG,GRAPHDICT[LANG]),id))
        if not os.path.exists(OUTFILENAME):
                subprocess.call(["gnuplot","/tmp/django/wikicount/scripts/gnuplot."+str(GRAPHDICT[LANG])])
                SFILE='/tmp/'+str(GRAPHDICT[LANG])+'.png'
                subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)

        return

def fnFindCategory(id):
        QUERY={'id':id}
        MAPQ=db.category.find({'_id':id})
        title=''
        utitle=''
        for name in MAPQ:
                        title=name['title']
                        s_title=string.replace(title,'_',' ')
                        t_title=s_title.encode('utf-8')
                        utitle=urllib2.unquote(t_title)
        return title, utitle

def fnFindImage(id):
        QUERY={'id':id}
        MAPQ=db.image.find({'_id':id})
        title=''
        utitle=''
        for name in MAPQ:
                        title=name['title']
                        s_title=string.replace(title,'_',' ')
                        t_title=s_title.encode('utf-8')
                        utitle=urllib2.unquote(t_title)


        return title, utitle

def fnFindName(LANG,id):
        QUERY={'id':id}
	CNAME=str(LANG)+"_hitsdaily"
        MAPQ=db[CNAME].find({'_id':id})
        title=''
        utitle=''
        for name in MAPQ:
                        title=name['title']
                        s_title=string.replace(title,'_',' ')
                        t_title=s_title.encode('utf-8')
                        utitle=urllib2.unquote(t_title)
        return title, utitle

def fnFormatName(title):
        s_title=string.replace(title,'_',' ')
        t_title=s_title.encode('utf-8')
        utitle=urllib2.unquote(t_title)
        return title, utitle
def fnReturnStringDate(DAY,MONTH,YEAR):
        DAY='%02d' % (DAY,)
        MONTH='%02d' % (MONTH,)
        RETSTR=str(YEAR)+"_"+str(MONTH)+"_"+str(DAY)
        return RETSTR

def fnGenTableArchive(id,place,LANG):
	send_list=[];
	CNAME=str(LANG)+'_mapPlace'
	QUERY={'_id':id}
	FINDQ=db[CNAME].find_one(QUERY)
	year=2013
	for month in range(1,13):
		for day in range(1,32):
			RETSTR=fnReturnStringDate(day,month,year)
			try:
				if FINDQ[RETSTR]>0 and FINDQ[RETSTR]<place:
					rec=str(str(year)+'/'+str(month)+'/'+str(day)+' '+str(FINDQ[RETSTR])+'\n')
					send_list.append(rec)
			except KeyError:
				continue
			except TypeError:
				continue
	return send_list

def fnGetDate():
	TODAY=date.today()
	DAY=TODAY.day
	MONTH=TODAY.month
	YEAR=TODAY.year
	return DAY,MONTH,YEAR

	
def fnGetHour():
	return time.strftime('%H')

def fnGetHourString(hour):
        HOUR='%02d' % (hour,)
        return HOUR

def fnGetMonthName():
	MONTHNAME=datetime.datetime.now().strftime("%B")
	return MONTHNAME

def fnLatestnews():
        ARTICLELIMIT=5
        latest_news_list = db.news.find().sort('date',-1).limit(ARTICLELIMIT)
        return latest_news_list

def fnMinusHour(HOUR):
        HOUR-=1
        if HOUR==-1:
                HOUR=23
        elif HOUR==-2:
                HOUR=22
        elif HOUR==-3:
                HOUR=21
        elif HOUR==-4:
                HOUR=20
        elif HOUR==-5:
                HOUR=19
        elif HOUR==-6:
                HOUR=18
        elif HOUR==-7:
                HOUR=17
        return HOUR
def fnAppendSitemap(id,LANG):
	out=open("/tmp/sitemap.xml","a")
	out.write("<url>\n")
	out.write("     <loc>http://www.wikitrends.info/'+str(LANG)+'/infoview/"+str(id)+"</loc>\n")
	out.write("     <changefreq>daily</changefreq>\n")
	out.write("	<priority>0.5</priority>\n")
	out.write("</url>\n")
	out.close()
	return
def fnOpenSitemap():
	out=open("/tmp/sitemap.xml","w")
	out.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
 	out.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
	out.close()
	return
def fnSetMemcache(KEYNAME,send_list,exptime):
	MEMCACHE_SERVERS=['127.0.0.1','10.62.13.235']
	mc1=memcache.Client(['127.0.0.1:11211'],debug=0)
	syslog.syslog('setting memcache key '+str(KEYNAME))
	mc1.set(KEYNAME,send_list,exptime)
	return
def GenInfoDailyGraph(id):
	DAY,MONTH,YEAR=fnGetDate()
	OFILE=open("/tmp/daily.log","w")
	for aMONTH in range(1,MONTH+1):
		for aDAY in range(1,31):
			strDAY=fnGetHourString(aDAY)
			strMONTH=fnGetHourString(aMONTH)
			SEARCHDATE="2013_"+str(strMONTH)+"_"+str(strDAY)
			OUTDATE="2013/"+str(strMONTH)+"/"+str(strDAY)
			RESULT=db.hitsdaily.find_one({"_id":id,SEARCHDATE:{"$gt":0}})
			try:
				OFILE.write(str(OUTDATE)+" "+str(RESULT[SEARCHDATE])+"\n")
			except TypeError:
				pass
	OFILE.close()
	fnDrawGraph(365,id)
				
	return
def GenInfoPage(id,LANG='en'):
	HOURGRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/hourly/'
        DAILYGRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/daily/'
        T25GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t25/'
        T50GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t50/'
        T100GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t100/'
        T500GRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t500/'
        T1KGRAPHDIRECTORY='http://www.wikitrends.info/static/images/'+str(LANG)+'/t1k/'

        if not os.path.exists(HOURGRAPHDIRECTORY):
                os.makedirs(HOURGRAPHDIRECTORY)
        if not os.path.exists(DAILYGRAPHDIRECTORY):
                os.makedirs(DAILYGRAPHDIRECTORY)
        if not os.path.exists(T25GRAPHDIRECTORY):
                os.makedirs(T25GRAPHDIRECTORY)
        if not os.path.exists(T50GRAPHDIRECTORY):
                os.makedirs(T50GRAPHDIRECTORY)
        if not os.path.exists(T100GRAPHDIRECTORY):
                os.makedirs(T100GRAPHDIRECTORY)
        if not os.path.exists(T500GRAPHDIRECTORY):
                os.makedirs(T500GRAPHDIRECTORY)
        if not os.path.exists(T1KGRAPHDIRECTORY):
                os.makedirs(T1KGRAPHDIRECTORY)

	#GenInfoDailyGraph(id)
	fnAppendSitemap(id,LANG)
	
	info_lt_25_list=[]
	info_lt_50_list=[]
	info_lt_100_list=[]
	info_lt_500_list=[]
	info_lt_1000_list=[]
	
	info_lt_25_list=fnGenTableArchive(id,26,LANG)
	info_lt_50_list=fnGenTableArchive(id,51,LANG)        
	info_lt_100_list=fnGenTableArchive(id,101,LANG)        
	info_lt_500_list=fnGenTableArchive(id,501,LANG)        
	info_lt_1000_list=fnGenTableArchive(id,1001,LANG)        

	T25FILE=open('/tmp/t25.log','w')
	T50FILE=open('/tmp/t50.log','w')
	T100FILE=open('/tmp/t100.log','w')
	T500FILE=open('/tmp/t500.log','w')
	T1KFILE=open('/tmp/t1k.log','w')

	for item in info_lt_25_list:
		T25FILE.write(item)
	for item in info_lt_50_list:
		T50FILE.write(item)
	for item in info_lt_100_list:
		T100FILE.write(item)
	for item in info_lt_500_list:
		T500FILE.write(item)
	for item in info_lt_1000_list:
		T1KFILE.write(item)
	
	T25FILE.close()
	T50FILE.close()
	T100FILE.close()
	T500FILE.close()
	T1KFILE.close()

	fnDrawGraph(25,id,LANG)
	fnDrawGraph(50,id,LANG)
	fnDrawGraph(100,id,LANG)
	fnDrawGraph(500,id,LANG)
	fnDrawGraph(1000,id,LANG)

		
	return


