import sys
sys.path.append('..')
from django.core.management import setup_environ
from timeinline import settings
from userside.models import *
from random import random,randrange
from math import exp
from datetime import datetime,timedelta
from django.utils import timezone

def poisson(lambd):
  L = exp(-lambd)
  k = 1
  p = 1

  u = random()
  p = p * u
  while p > L:
    k = k + 1
    u = random()
    p = p * u
  return k - 1


def main():
  comp = Company.objects.get(id=7)
  t_year = 2012
  t_month = 4
  t_week = 15
  t_id = 206
  for i in range(0,20):
    cust = Customer.objects.get(id=t_id+i)
    for d in range(0,7):
      for h in range(0,24):
	rm = randrange(0,60,1)
	rwait = poisson(3)
	rcall = poisson(10)
	call_start = datetime(t_year,t_month,t_week+d,hour=h,minute=rm,tzinfo=timezone.utc)
	call_ans   = call_start + timedelta(minutes=rwait)
	call_end   = call_start + timedelta(minutes=rwait+rcall)
	c = Call(customer=cust,company=comp,rep_id=1,callstart=call_start,callanswered=call_ans,callend=call_end)
	c.save()

	

if __name__ == '__main__':
  setup_environ(settings)
  main()
