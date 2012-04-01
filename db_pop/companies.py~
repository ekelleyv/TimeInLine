from django.core.management import setup_environ
from timeinline import settings
from userside.models import *

setup_environ(settings)

for i in range(5):
  rname = "company"+str(i)
  c = Company(name=rname)
  c.save()


