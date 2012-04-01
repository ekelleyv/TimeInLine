import sys
sys.path.append('..')
from django.core.management import setup_environ
from timeinline import settings
from userside.models import *
from random import randrange
from datetime import datetime,timedelta
from django.utils import timezone

setup_environ(settings)

this_year  = 2012
this_month = 3
this_week  = 18
for i in range(1,201):
  cust = Customer.objects.get(id=i)
  for j in range(2):
    rc = randrange(1,6,1)
    rcomp = Company.objects.get(id=rc)
    rd = this_week + randrange(0,7,1)
    rh = randrange(9,18,1)
    rm = randrange(0,60,1)
    rwait = randrange(0,20,1)
    rcall = randrange(0,10,1)
    call_start = datetime(this_year,this_month,rd,hour=rh,minute=rm,tzinfo=timezone.utc)
    call_ans   = call_start + timedelta(minutes=rwait)
    call_end   = call_start + timedelta(minutes=rwait+rcall)
    c = Call(customer=cust,company=rcomp,callstart=call_start,callanswered=call_ans,callend=call_end)
    c.save()

