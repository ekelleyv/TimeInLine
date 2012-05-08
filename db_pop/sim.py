import sys
sys.path.append('..')
from django.core.management import setup_environ
from timeinline import settings
from userside.models import *
from userside.views import *
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

def process_queue(calls,in_serv):
  while len(calls) > 0:
    c_old = in_serv.pop(0)
    c_new = calls.pop(0)
    rwait = poisson(3)
    rcall = poisson(10)
    c_old.callend = c_old.callanswered + timedelta(minutes=rcall)
    c_old.save()

    c_new.callanswered = c_new.callstart + timedelta(minutes=rwait)
    c_new.rep_id = c_old.rep_id
    c_new.save()
    in_serv.append(c_new)

def process_rest(calls, in_serv):
  for c in calls:
    rwait = poisson(3)
    rcall = poisson(10)
    rrep  = randrange(1,21,1)
    c.callanswered = c.callstart + timedelta(minutes=rwait)
    c.callend      = c.callanswered + timedelta(minutes=rcall)
    c.rep_id = rrep
    c.save()

  for c in in_serv:
    rcall = poisson(10)
    c.callend = c.callanswered + timedelta(minutes=rcall)
    c.save()

  return

def main():
  comp_id = 1 #long(raw_input("Company: "))
  n_reps  = working_reps(comp_id)
  total_custs = len(Customer.objects.all())

  soq     = long(raw_input("Size of Queue(max ##): "))
  if soq > total_custs - n_reps:
    print "Queue is too big"
    return

  today  = datetime.today()
  comp = Company.objects.get(id=comp_id)

  n_custs = soq + n_reps 
  base_r = 1
  base_c = 1 
  custs = []
  # retrieve customers
  for i in range(0,n_custs):
    cust = Customer.objects.get(id=base_c+i)
    custs.append(cust)

  calls = []
  # start calls
  for i in range(0,n_custs):
    t = datetime.today()
    m = t.minute-n_custs+i
    h = t.hour
    if m < 0:
      m = 60 + m
      h -= 1
    elif m > 59:
      m = m - 60
      h += 1
    call_start = datetime(t.year,t.month,t.day,hour=h,minute=m,tzinfo=timezone.utc)
    c = Call(customer=custs[i], company=comp, callstart=call_start)
    c.save()
    calls.append(c)

  in_serv = []
  # answer all except for soq
  for i in range(0,n_reps):
    c = calls.pop(0)
    rwait = poisson(3)
    c.callanswered = c.callstart + timedelta(minutes=rwait)
    c.rep_id = base_r + i
    c.save()
    in_serv.append(c)

  avg_serv = avg_serv_rate(comp)
  
  # enter to service and answer a call
  # 'c' to finish the script
  while len(calls) > 0:
    for c in calls:
      number = Customer.objects.get(id=c.customer_id).phone_number
      pos = place_in_line(comp,number)
      est = round(est_wait(avg_serv,n_reps,pos),0)
      print number, pos, est
    s = str(raw_input("Process Call? "))
    if s == "c":
      process_queue(calls,in_serv)
      break
    c_old = in_serv.pop(0)
    c_new = calls.pop(0)
    rwait = poisson(3)
    rcall = poisson(10)
    c_old.callend = c_old.callanswered + timedelta(minutes=rcall)
    c_old.save()

    c_new.callanswered = c_new.callstart + timedelta(minutes=rwait)
    c_new.rep_id = c_old.rep_id
    c_new.save()
    in_serv.append(c_new)

  str(raw_input("Service remaining calls?"))
  process_rest(calls,in_serv)

if __name__ == '__main__':
  setup_environ(settings)
  main()
