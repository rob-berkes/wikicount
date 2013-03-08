import syslog
import os
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
