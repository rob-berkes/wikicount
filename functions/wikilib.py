import syslog
import urllib2
import os
import string
import datetime 
from pymongo import Connection 
import memcache

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

def FormatName(title):
        s_title=string.replace(title,'_',' ')
        t_title=s_title.encode('utf-8')
        utitle=urllib2.unquote(t_title)
        return title, utitle

def GenInfoPage(id,YEAR,MONTHNAME):
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

        for result in DFINDQ:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                send_list.append(rec)
        for result in FINDQ:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                send_list.append(rec)

        LT50KQ=db[thCN].find(Q50K)
        for result in D50KFINDQ:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                info_lt50k_list.append(rec)
        for result in LT50KQ:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                info_lt50k_list.append(rec)

        LT5KQ=db[thCN].find(Q5K)
        for result in D5KFINDQ:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                info_lt5k_list.append(rec)
        for result in LT5KQ:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                info_lt5k_list.append(rec)

        LT500=db[thCN].find(Q500)
        for result in D500FINDQ:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                info_lt500_list.append(rec)
        for result in LT500:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                info_lt500_list.append(rec)

	LT50=db[thCN].find(Q50)
        for result in D50FINDQ:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                info_lt50_list.append(rec)
        for result in LT50:
                rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
                info_lt50_list.append(rec)


        mc.set(INFOVIEW_KEY,send_list,60*60*12)
        mc.set(INFOVIEWLT_KEY,info_lt50k_list,60*60*12)
        mc.set(INFOVIEWLT5K_KEY,info_lt5k_list,60*60*12)
        mc.set(INFOVIEWLT500_KEY,info_lt500_list,60*60*12)
        mc.set(INFOVIEWLT50_KEY,info_lt50_list,60*60*12)
        return

