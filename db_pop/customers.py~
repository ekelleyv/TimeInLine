import sys
sys.path.append('..')
from django.core.management import setup_environ
from timeinline import settings
from userside.models import *

setup_environ(settings)

base = 1111110000
for i in range(200):
  num = base + i
  c = Customer(phone_number=num)
  c.save()

