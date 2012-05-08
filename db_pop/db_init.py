import sys
sys.path.append('..')
from django.core.management import setup_environ
from timeinline import settings
from userside.models import *
from random import random,randrange,randint
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

def rwait_time(d,h):
	r = 3
	if d in [1,5]:
		r += 3
	if h in [11,12,16,17,18]:
		r += 5
	return poisson(r)

def create_calls(comp):
	t_year = 2012
	t_month = 4
	t_week = 22 
	for i in range(1,21):
		print "cust: ", i
		cust = Customer.objects.get(id=i)
		for d in range(0,7):
			for h in range(0,24):
				r_minute = randrange(0,60,1)
				rwait = rwait_time(d,h) 
				rcall = poisson(10)
				call_start = datetime(t_year,t_month,t_week+d,hour=h,minute=r_minute,tzinfo=timezone.utc)
				call_ans = call_start + timedelta(minutes=rwait)
				call_end = call_start + timedelta(minutes=rwait+rcall)
				c = Call(customer = cust, company=comp, rep_id=1, callstart=call_start, callanswered=call_ans, callend=call_end)
				c.save()

def create_custs():
	for i in range(0,50):
		rnum = randint(1000000000,9999999999)
		c = Customer(phone_number=rnum)
		c.save()

def create_reps(comp, cc):  
	for i in range(1,21):
		r = Representative(company=comp, callcenter=cc, internal_id=i)
		r.save()

def main():
	# create a company
	#comp_name = "Company 1"
	#comp = Company(name=comp_name)
	#comp.save()

	# create a callcenter
	#cc_name = "Callcenter 1"
	#cc = CallCenter(name=cc_name,company=comp)
	#cc.save()

	# create 20 reps
	#create_reps(comp,cc)

	# create 50 customers
	#create_custs()

	# create calls
	comp = Company.objects.get(id=1)
	create_calls(comp)

if __name__ == '__main__':
	setup_environ(settings)
	main()
