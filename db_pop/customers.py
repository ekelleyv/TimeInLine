import sys
sys.path.append('..')
from django.core.management import setup_environ
from timeinline import settings
from userside.models import *

setup_environ(settings)

base = 35 
for i in range(16):
	num = base + i
	c = Customer(phone_number=num)
	c.save()

