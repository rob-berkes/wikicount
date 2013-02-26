#!/usr/bin/python
import memcache 
import string 
import random
from pymongo import Connection
from datetime import date
from datetime import time
import datetime
import subprocess
import syslog
import os

conn=Connection('10.115.126.7')
db=conn.wc
mc=memcache.Client(['127.0.0.1:11211'],debug=0)
TODAY=date.today()
DAY=TODAY.day
MONTH=TODAY.month
YEAR=TODAY.year
MONTHNAME=datetime.datetime.now().strftime("%B")


def returnHourString(hour):
	HOUR='%02d' % (hour,)
	return HOUR
def GenHourlyGraph(id):
	RESULT1=db.hitshourly.find_one({"_id":str(id)})
	OFILE=open('output.log','w')
	try:
		for i in range(0,24):
			HOUR=returnHourString(i)	
			try:
				OFILE.write(str(HOUR)+' '+str(RESULT1[HOUR])+'\n')
			except TypeError:
				pass 
	except KeyError:
		pass
	OFILE.close()
	subprocess.call(["gnuplot","gnuplot.plot"])
	OUTFILENAME='/tmp/django/wikicount/static/images/hourly/'+str(id)+'.png'
	SFILE='/tmp/django/wikicount/introduction.png'
	subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	return
def GenInfoPage(id):
	GenHourlyGraph(id)
	MONTHNAME=datetime.datetime.now().strftime("%B")
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
        
	OFILE250K=open("/tmp/t250k.log","w")	
	for result in DFINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE250K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	send_list.append(rec)
        for result in FINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE250K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	send_list.append(rec)
	OFILE250K.close()
	OUTFILENAME='/tmp/django/wikicount/static/images/t250k/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.250k"])
		SFILE='/tmp/t250k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.250k"])
		SFILE='/tmp/t250k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
			
	OFILE50K=open("/tmp/t50k.log","w")	
	LT50KQ=db[thCN].find(Q50K)
        for result in D50KFINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE50K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt50k_list.append(rec)
        for result in LT50KQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE50K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt50k_list.append(rec)
	OFILE50K.close()
	OUTFILENAME='/tmp/django/wikicount/static/images/t50k/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.50k"])
		SFILE='/tmp/t50k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.50k"])
		SFILE='/tmp/t50k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)

	OFILE5K=open("/tmp/t5k.log","w")	
	LT5KQ=db[thCN].find(Q5K)
        for result in D5KFINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE5K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt5k_list.append(rec)
        for result in LT5KQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE5K.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt5k_list.append(rec)
	OFILE5K.close()
	OUTFILENAME='/tmp/django/wikicount/static/images/t5k/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.5k"])
		SFILE='/tmp/t5k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.5k"])
		SFILE='/tmp/t5k.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)

	LT500=db[thCN].find(Q500)
	OFILE500=open("/tmp/top500.log","w")
        for result in D500FINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE500.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt500_list.append(rec)
        for result in LT500:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE500.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt500_list.append(rec)
	OFILE500.close()	
	OUTFILENAME='/tmp/django/wikicount/static/images/t500/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.500"])
		SFILE='/tmp/top500.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.500"])
		SFILE='/tmp/top500.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)

	LT50=db[thCN].find(Q50)
	OFILE50=open("/tmp/top50.log","w")
        for result in D50FINDQ:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE50.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt50_list.append(rec)
        for result in LT50:
	        rec={'d':str(result['d']),'m':str(result['m']),'y':str(result['y']),'place':str(result['place'])}
		OFILE50.write(str(rec['y'])+'/'+str(rec['m'])+'/'+str(rec['d'])+' '+str(rec['place'])+'\n')
        	info_lt50_list.append(rec)
	OFILE50.close()	
	OUTFILENAME='/tmp/django/wikicount/static/images/t50/'+str(id)+'.png'
	if os.path.lexists(OUTFILENAME) and random.randint(0,20)==10:
		subprocess.call(["gnuplot","gnuplot.50"])
		SFILE='/tmp/top50.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)
	elif not os.path.lexists(OUTFILENAME):
		subprocess.call(["gnuplot","gnuplot.50"])
		SFILE='/tmp/top50.png'
		subprocess.Popen("mv "+str(SFILE)+" "+str(OUTFILENAME),shell=True)


        mc.set(INFOVIEW_KEY,send_list,60*60*12)
	mc.set(INFOVIEWLT_KEY,info_lt50k_list,60*60*12)
	mc.set(INFOVIEWLT5K_KEY,info_lt5k_list,60*60*12)
	mc.set(INFOVIEWLT500_KEY,info_lt500_list,60*60*12)
	mc.set(INFOVIEWLT50_KEY,info_lt50_list,60*60*12)
	return


syslog.syslog('draw_trending.py: starting....')
send_list=[]    
TRENDING_QUERY=mc.get('TRENDING_LIST_QUERY')
for p in TRENDING_QUERY:
	rec={'title':p['title'],'place':p['place'],'Hits':p['Hits']%1000,'linktitle':p['linktitle'],'id':p['id']}
        send_list.append(rec)
	GenInfoPage(p['id'])
syslog.syslog('draw_trending.py: done!')
mc.set('TRENDING_LIST_QUERY',send_list,1800)


