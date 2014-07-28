from pymongo import Connection
from datetime import date
from datetime import time
import syslog
from lib import wikilib


conn=Connection('10.164.95.114')
db=conn.wc
TODAY=date.today()
DAY=TODAY.day
MONTH=TODAY.month
YEAR=TODAY.year
MONTHNAME=TODAY.strftime("%B")
send_list=[]

thCN='tophits'+str(YEAR)+MONTHNAME
PASTTABLES=['tophits2013February']
for COLLECTION in PASTTABLES:
	RESULTSET=db.command({'distinct':COLLECTION,'key':'d'})
	if COLLECTION=='tophits':
		MONTH=1
		YEAR=2013
	elif COLLECTION=='tophits2013February':
		MONTH=2
		YEAR=2013
	for d in RESULTSET['values']:
	        rec={'d':d,'m':MONTH,'y':YEAR,'stry':str(YEAR),'strm':str(MONTH),'strd':str(d)}
	        QUERY={'d':int(d),'m':int(MONTH),'y':int(YEAR)}
	        DAYKEY='toplist'+str(YEAR)+str(MONTH)+str(d)
	        page_list=[]
	        PAGERESULTSET=db[COLLECTION].find(QUERY).sort('place',1).limit(100)
	        syslog.syslog('mc-archives: '+str(DAYKEY)+' '+str(QUERY)+' count: '+str(PAGERESULTSET.count()))
	        for row in PAGERESULTSET:
		        title, utitle=wikilib.fnFindName(row['id'])

	                prec={'place':row['place'],'Hits':row['Hits'],'title':title ,'id':str(row['id']),'linktitle':utitle}
	                page_list.append(prec)
	                wikilib.GenInfoPage(row['id'])
		syslog.syslog('mc-archives: Now setting mc key '+str(DAYKEY)+' of length '+str(len(page_list)))
	        wikilib.fnSetMemcache(DAYKEY,page_list,60*60)
	        send_list.append(rec)
	mc.set('mcdpDaysList'+str(MONTH)+str(YEAR),send_list,60*60*24*60)

