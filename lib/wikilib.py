import urllib2
import os
import string
import datetime 
from datetime import date
from pymongo import Connection 
import time
import subprocess 
import syslog
import Gnuplot, Gnuplot.funcutils

MONGO_IP = '10.219.4.172'
conn = Connection(MONGO_IP)
db = conn.wc

LLIST = { 'ru':'Russian Wikipedia',
	'en':'English Wikipedia',
	'ja':'Japanese Wikipedia',
	'zh':'Chinese Wikipedia',
        'hy':'Armenian Wikipedia',
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
def fnDoGraphDrawing(type,id,LANG):
	GRAPHDICT={'25':'t25',
                  '50':'t50',
                  '100':'t100',
                  '500':'t500',
                  '1000':'t1k',
                  '24':'hourly',
		  '365':'daily'}
	OUTFILENAME="/tmp/django/wikicount/static/images/"+str(LANG)+"/"+str(GRAPHDICT[str(type)])+"/"+str(id)+".png" 
	g=Gnuplot.Gnuplot()
	title,utitle=fnFindName(LANG,id)
	g('set terminal png size 480,300')
	g('set object 3 rectangle from screen 0,0 to screen 1,1 fillcolor rgb"#aaaaff" behind')
	if len(utitle) < 17:
		g('set object 1 rectangle from graph 0.41,0.91 \\')
		g('to graph 0.98,0.98 fillstyle solid 1.0 noborder \\')
		g('fc rgb"#cccccc"')		#key-box shadow
		g('set object 2 rectangle from graph 0.40,0.90 \\')
		g('to graph 0.99,0.99 fc rgb"#ffffff"')    #key-box
	else:
		g('set object 1 rectangle from graph 0.01,0.91 \\')
		g('to graph 0.98,0.98 fillstyle solid 1.0 noborder \\')
		g('fc rgb"#cccccc"')		#key-box shadow
		g('set object 2 rectangle from graph 0.00,0.90 \\')
		g('to graph 0.99,0.99 fc rgb"#ffffff"')    #key-box
		
	if type==365:
		LLIST=fnGenTableArchive(id,365,LANG)
		g('set xtics format '+'\"'+'%b %d'+'\"')
		g('set key font ",1"')	
		g('set style line 1 lc rgb "#ff0000" lt 1 lw 2 pt 2 ps 1.5')
		g('set style function linespoints ')
		g('set title "Hits Per Day"')
		g('set xdata time')
		g('set timefmt "%s"')
		g('set output '+'\"'+OUTFILENAME+'\"')
		g.plot(Gnuplot.Data(LLIST,using="1:2",with_="linespoints ls 1",title=utitle))
	elif type==24:
		LLIST=fnGenTableArchive(id,24,LANG)
		g('set style data boxes')
		g('set style fill solid 0.6')
		g('set xdata time')
		g('set title "Hits Per Hour"')
		g('set encoding iso_8859_1')
		g('set xtics format '+'\"'+'%H'+'\"')	
		g('set timefmt "%H"')
		g('set xlabel "Hour of Day(UTC)"')
		g('set output '+'\"'+OUTFILENAME+'\"')
		if len(LLIST)>0:
			g.plot(Gnuplot.Data(LLIST,using="1:2",title=str(utitle)))		
	return 
def fnDrawGraph(type,id,LANG):
	GRAPHDICT={'25':'t25',
                  '50':'t50',
                  '100':'t100',
                  '500':'t500',
                  '1000':'t1k',
                  '365':'daily'}
        subprocess.call(["gnuplot","/tmp/django/wikicount/scripts/gnuplot."+str(GRAPHDICT[str(type)])])

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
	test_list={};
	CNAME=str(LANG)+'_hitsdaily'
	QUERY={'_id':str(id)}
	year=2013
	if place==365:
		FINDQ=db[CNAME].find_one(QUERY)
		for month in range(1,13):
			for day in range(1,32):
				RETSTR=fnReturnStringDate(day,month,year)
				try:
					if int(FINDQ[RETSTR])>0 :
						DATEEPOCH=datetime.datetime(int(year),int(month),int(day)).strftime('%s')
						rec=(DATEEPOCH,int(FINDQ[RETSTR]))
						send_list.append(rec)
	#					send_list[str(year)+'/'+str(month)+'/'+str(day)]=FINDQ[RETSTR]
				except KeyError:
					continue
				except TypeError:
					continue
	elif place==24:
		HHDT=str(LANG)+"_hitshourly"
		FINDLIST=db[HHDT].find_one(QUERY)
		for a in range(0,24):
			try:
				rec=(a, int(FINDLIST[str(a)]))
				send_list.append(rec)
			except KeyError:
				continue
			except TypeError:
				continue
			except IndexError:
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
	#mc=memcache.Client(['127.0.0.1:11211'],debug=0)
	syslog.syslog('setting memcache key '+str(KEYNAME))
	#mc1.set(KEYNAME,send_list,exptime)
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
	PID=os.getpid()
	fnAppendSitemap(id,LANG)
	
	fnDoGraphDrawing(365,id,LANG)
	fnDoGraphDrawing(24,id,LANG)

		
	return

