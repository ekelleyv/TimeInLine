import sys
sys.path.append('..')
from django.core.management import setup_environ
from timeinline import settings
from userside.models import *

setup_environ(settings)

c = 7
cc = 2
internal = 2
for i in range(19):
  r = Representative(company_id=c,callcenter_id=cc,internal_id=internal)
  r.save()
  internal = internal + 1

