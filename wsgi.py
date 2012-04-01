import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'timeinline.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
