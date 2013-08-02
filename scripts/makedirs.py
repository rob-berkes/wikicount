import os
LANGS=['it.q','pl.q','ru.q','zh.q']
PATHS=['daily','hourly','t25','t50','t100','t500','t1k']
for lang in LANGS:
	for path in PATHS:
		DIRMAKE="/tmp/django/wikicount/static/images/"+str(lang)+"/"+str(path)
		if not os.path.exists(DIRMAKE):
			os.makedirs(DIRMAKE)

