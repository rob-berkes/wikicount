import syslog
import urllib2
import os
import string
import datetime 
from pymongo import Connection 
import memcache
import time

mc=memcache.Client(['127.0.0.1:11211'],debug=0)
conn=Connection('10.115.126.7')
db=conn.wc

def fnLaunchNextJob(CURJOBNAME):
	if CURJOBNAME=='set_vars':
		syslog.syslog('Launching image draw for trending...')
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_draw_trending_graphs.py')
	elif CURJOBNAME=='trending':
		syslog.syslog('Launching threehour images script...') 
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_draw_threehour.py')
	elif CURJOBNAME=='threehour':
		syslog.syslog('Launching random graph image draw script...')
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_draw_random_graphs.py')
	elif CURJOBNAME=='random':
		syslog.syslog('Launching cold images script...')
		os.system('/usr/bin/python /tmp/django/wikicount/scripts/memcache_draw_cold.py')
	elif CURJOBNAME=='cold':
		syslog.syslog('All done with memcached for now!')
	return 
def fnLatestnews():
        ARTICLELIMIT=5
        latest_news_list = db.news.find().sort('date',-1).limit(ARTICLELIMIT)
        return latest_news_list

def fnFormatName(title):
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
def fnMinusHour(HOUR):
        HOUR-=7
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


def fnGetHourString(hour):
        HOUR='%02d' % (hour,)
        return HOUR


def fnGenTableArchive(TABLENAME,id,place):
	send_list=[];
	QUERY={'id':id,'place':place}
	FINDQ=db[TABLENAME].find(QUERY)
	for result in FINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
        	send_list.append(rec)

	return send_list

def fnGetHour():
	return time.strftime('%H')

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



        mc.set(INFOVIEW_KEY,send_list,60*60*12)
	mc.set(INFOVIEWLT_KEY,info_lt50k_list,60*60*12)
	mc.set(INFOVIEWLT5K_KEY,info_lt5k_list,60*60*12)
	mc.set(INFOVIEWLT500_KEY,info_lt500_list,60*60*12)
	mc.set(INFOVIEWLT50_KEY,info_lt50_list,60*60*12)
	return


