from pymongo import Connection
import memcache
from datetime import date
from datetime import time
import syslog
from functions import wikilib


conn=Connection('10.37.11.218')
db=conn.wc
mc=memcache.Client(['127.0.0.1:11211'],debug=0)
TODAY=date.today()
DAY=TODAY.day
MONTH=TODAY.month
YEAR=TODAY.year
MONTHNAME=TODAY.strftime("%B")
send_list=[]

thCN='tophits'+str(YEAR)+MONTHNAME
PASTTABLES=['tophits','tophits2013February']
for COLLECTION in PASTTABLES:
	RESULTSET=db.command({'distinct':COLLECTION,'key':'d'})
	if COLLECTION=='tophits':
		MONTH=12
		YEAR=2012
	elif COLLECTION=='tophitsFebruary2013':
		MONTH=2
		YEAR=2013
	for d in RESULTSET['values']:
	        rec={'d':d,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(d)}
	        QUERY={'d':int(d),'m':int(MONTH),'y':int(YEAR)}
	        DAYKEY='toplist'+str(YEAR)+str(MONTH)+str(d)
	        page_list=[]
	        PAGERESULTSET=db[COLLECTION].find(QUERY).sort('place',1).limit(100)
	        syslog.syslog('memcache-monthly: '+str(DAYKEY)+' '+str(QUERY)+' count: '+str(PAGERESULTSET.count()))
	        for row in PAGERESULTSET:
		        title, utitle=wikilib.fnFindName(row['id'])

	                prec={'place':row['place'],'Hits':row['Hits'],'title':title ,'id':str(row['id']),'linktitle':utitle}
	                wikilib.GenInfoPage(row['id'])
	                page_list.append(prec)
	                mc.set(DAYKEY,page_list,60*60*24*60)
	        send_list.append(rec)
	mc.set('mcdpDaysList'+str(MONTH)+str(YEAR),send_list,60*60*24*60)

