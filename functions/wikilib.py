import syslog
import urllib2
import os
import string
import datetime 
from datetime import date
from pymongo import Connection 
import memcache
import time
import subprocess 

conn=Connection('10.37.11.218')
db=conn.wc

def fnDrawGraph(type,id):
        if type==250:
                OUTFILENAME='/tmp/django/wikicount/static/images/t250k/'+str(id)+'.png' 
                if not os.path.lexists(OUTFILENAME):
                        subprocess.call(["gnuplot","/tmp/django/wikicount/scripts/gnuplot.250k"])
                        SFILE='/tmp/t250k.png'
                        subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
        elif type==50000:
                OUTFILENAME='/tmp/django/wikicount/static/images/t50k/'+str(id)+'.png' 
                if not os.path.lexists(OUTFILENAME):
                        subprocess.call(["gnuplot","/tmp/django/wikicount/scripts/gnuplot.50k"])
                        SFILE='/tmp/t50k.png'
                        subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
        elif type==5000:
                OUTFILENAME='/tmp/django/wikicount/static/images/t5k/'+str(id)+'.png' 
                if not os.path.lexists(OUTFILENAME):
                        subprocess.call(["gnuplot","/tmp/django/wikicount/scripts/gnuplot.5k"])
                        SFILE='/tmp/t5k.png'
                        subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
        elif type==500:
                OUTFILENAME='/tmp/django/wikicount/static/images/t500/'+str(id)+'.png' 
                if not os.path.lexists(OUTFILENAME):
                        subprocess.call(["gnuplot","/tmp/django/wikicount/scripts/gnuplot.500"])
                        SFILE='/tmp/t500.png'
                        subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
        elif type==50:
                OUTFILENAME='/tmp/django/wikicount/static/images/t50/'+str(id)+'.png' 
                if not os.path.lexists(OUTFILENAME):
                        subprocess.call(["gnuplot","/tmp/django/wikicount/scripts/gnuplot.50"])
                        SFILE='/tmp/t50.png'
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

def fnFindName(id):
        QUERY={'id':id}
        MAPQ=db.hitsdaily.find({'_id':id})
        latest_news_list = fnLatestnews()
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

def fnGenTableArchive(TABLENAME,id,place):
	send_list=[];
	QUERY={'id':id,'place':{'$lt':place}}
	FINDQ=db[TABLENAME].find(QUERY)
	for result in FINDQ:
		rec=str(item['y'])+'/'+str(item['m'])+'/'+str(item['d'])+' '+str(item['place'])+'\n'
        	send_list.append(rec)
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

def fnLaunchNextJob(CURJOBNAME):
	if CURJOBNAME=='set_cold':
		syslog.syslog('Launching image draw for day...')
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_set_day.py')
	elif CURJOBNAME=='set_day':
		syslog.syslog('Launching debuts images script...') 
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_set_debuts.py')
	elif CURJOBNAME=='set_debuts':
		syslog.syslog('Launching last hour memcache  script...')
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_set_lasthour.py')
	elif CURJOBNAME=='set_lasthour':
		syslog.syslog('Launching memcache random images script...')
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_set_random.py')
	elif CURJOBNAME=='set_random':
		syslog.syslog('Launching threehour rolling avg script..')
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_set_threehour.py')
	elif CURJOBNAME=='set_threehour':
		syslog.syslog('Launching trending script....')
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_set_trending.py')
	elif CURJOBNAME=='set_trending':
		syslog.syslog('All done with memcached for now!')
	return 

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
def fnSetMemcache(KEYNAME,send_list,exptime):
	MEMCACHE_SERVERS=['127.0.0.1','10.62.13.235']
	mc1=memcache.Client(['127.0.0.1:11211'],debug=0)
	mc1.set(KEYNAME,send_list,exptime)
	return
def GenInfoPage(id):
	INFOVIEW_KEY='infoview_'+str(id)
	INFOVIEWLT_KEY='infoviewlt_'+str(id)
	INFOVIEWLT5K_KEY='infoviewlt5k_'+str(id)
	INFOVIEWLT500_KEY='infoviewlt500_'+str(id)
	INFOVIEWLT50_KEY='infoviewlt50_'+str(id)
	MONTHLIST=['tophits','tophits2013February','tophits2013March']
	send_list=[]
	info_lt50k_list=[]
	info_lt5k_list=[]
	info_lt500_list=[]
	info_lt50_list=[]
	for MONTH in MONTHLIST:
		send_list+=fnGenTableArchive(MONTH,id,250001)
		info_lt50k_list+=fnGenTableArchive(MONTH,id,50001)        
		info_lt5k_list+=fnGenTableArchive(MONTH,id,5001)        
		info_lt500_list+=fnGenTableArchive(MONTH,id,501)        
		info_lt50_list+=fnGenTableArchive(MONTH,id,51)        

	T50KFILE=open('/tmp/t50k.log','w')
	T250FILE=open('/tmp/t250k.log','w')
	T50FILE=open('/tmp/t50.log','w')
	T500FILE=open('/tmp/t500.log','w')
	T5KFILE=open('/tmp/t5k.log','w')

	for item in send_list:
		T250FILE.write(item)
	for item in info_lt50k_list:
		T50KFILE.write(item)
	for item in info_lt5k_list:
		T5KFILE.write(item)
	for item in info_lt500_list:
		T500FILE.write(item)
	for item in info_lt50_list:
		T50FILE.write(item)
	
	T50KFILE.close()
	T5KFILE.close()
	T500FILE.close()
	T50FILE.close()
	T250FILE.close()

	fnDrawGraph(50000,id)
	fnDrawGraph(5000,id)
	fnDrawGraph(500,id)
	fnDrawGraph(50,id)
	fnDrawGraph(250,id)

		
#        fnSetMemcache(INFOVIEW_KEY,send_list,60*60*12)
#	fnSetMemcache(INFOVIEWLT_KEY,info_lt50k_list,60*60*12)
#	fnSetMemcache(INFOVIEWLT5K_KEY,info_lt5k_list,60*60*12)
#	fnSetMemcache(INFOVIEWLT500_KEY,info_lt500_list,60*60*12)
#	fnSetMemcache(INFOVIEWLT50_KEY,info_lt50_list,60*60*12)
	return


