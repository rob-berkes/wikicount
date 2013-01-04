import os
import sys

os.environ('DJANGO_SETTINGS_MODULE')='settings.py'

import django.core.handlers.wsgi
application=django.core.handlers.wsgi.WSGIHandler()

path='/tmp/django/wikicount/' 
if path not in sys.path:
	sys.path.append(path)
