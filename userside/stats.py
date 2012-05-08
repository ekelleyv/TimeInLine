
from userside.models import *
from django.http import HttpResponse
from datetime import datetime, timedelta

#Returns all of the active calls for a given company
def active_calls(company_id):
	calls = Call.objects.filter(company_id = company_id, callanswered__isnull=True, callend__isnull=True)
	return calls

def picked_up(company_id, caller_id):
	customer = Customer.objects.get(phone_number = caller_id)
	calls = active_calls(company_id)
	try:
		picked_up_call = Calls.object.get(customer = customer, callanswered__isnull=False)
		return True
	except:
		return False

def place_in_line(company_id, caller_id):
	customer = Customer.objects.get(phone_number = caller_id)
	
	if Call.objects.filter(customer = customer, company_id = company_id, 
		  callanswered__isnull=True, callend__isnull=True) == []:
		return None
	
	calls = active_calls(company_id)
	
	current_calls = Call.objects.filter(customer = customer, callanswered__isnull=True, callend__isnull=True)
	if not current_calls:
		return 0
	current_call = current_calls.order_by('-callstart')[0]
	count = 1
	for call in calls:
		if call.callstart < current_call.callstart:
			count = count + 1
	return count

def active_company(caller_id):
	curr_customer = Customer.objects.get(phone_number = caller_id)
	calls = Call.objects.filter(customer = curr_customer, callend__isnull=True)
	if not calls:
		return None
	return calls[0].company_id

# note: need to add attr to Representative: active?
def working_reps(company_id):
	reps = Representative.objects.filter(company_id = company_id)
	return len(reps)


##########################################################

# returns timedelta/minutes
def avg_wait(company_id, retMinutes):
	sums, counts = sum_wait_by_day_hour(company_id, retMinutes)
	if sums is None:
		return None
	sum = 0 if retMinutes else timedelta(0)
	count = 0
	for i in range(7):
		for j in range(24):
			sum += sums[i][j]
			count += counts[i][j]
	if count == 0:
		avg = 0 if retMinutes else timedelta(0)
	else: 
		 avg = sum / count
	return avg

# return list (0-23) of timedeltas/minutes
def avg_wait_by_hour(company_id, retMinutes):
		sums, counts = sum_wait_by_day_hour(company_id, retMinutes)
		if sums is None:
				return None
		avg_hour = [0]*24 if retMinutes else [timedelta(0)]*24
		for j in range(24):
				sum = 0 if retMinutes else timedelta(0)
				count = 0
				for i in range(7):
						sum += sums[i][j]
						count += counts[i][j]
				if count == 0:
						avg_hour[j] = 0 if retMinutes else timedelta(0)
				else:
						avg_hour[j] = sum / count
		return avg_hour

# return list (0-6) of timedeltas/minutes
def avg_wait_by_day(company_id, retMinutes):
		sums, counts = sum_wait_by_day_hour(company_id, retMinutes)
		if sums is None:
				return None
		avg_day = [0]*7 if retMinutes else [timedelta(0)]*7
		for i in range(7):
				sum = 0 if retMinutes else timedelta(0)
				count = 0
				for j in range(24):
						sum += sums[i][j]
						count += counts[i][j]
				if count == 0:
						avg_day[i] = 0 if retMinutes else timedelta(0)
				else: 
						avg_day[i] = sum / count 
		return avg_day

# return 7 lists of 24 timedeltas/minutes
def avg_by_day_hour(company_id, retMinutes, retWait):
	if retWait:
		sums, counts = sum_wait_by_day_hour(company_id, retMinutes)
	else:
		sums, counts = sum_serv_by_day_hour(company_id, retMinutes)
	
	if sums is None:
		return None
	avg_day_hour = []
	if retMinutes:
		for i in range(7):
			avg_day_hour.append([0]*24)
	else:
		for i in range(7):
			avg_day_hour.append([timedelta(0)]*24)
	for i in range(7):
		for j in range(24):
			if counts[i][j] == 0:
				avg_day_hour[i][j] = 0 if retMinutes else timedelta(0)
			else:
				avg_day_hour[i][j] = sums[i][j] / counts[i][j]
	return avg_day_hour

##########################################################

# returns tuple: (7 lists of 24 timedeltas/minutes, 7 lists of 24 counts)
# excludes active calls and currently waiting
def sum_wait_by_day_hour(company_id, retMinutes):
	calls = Call.objects.filter(company_id=company_id, callstart__isnull=False, callend__isnull=False)
	if len(calls) == 0:
		return None, None
	
	sum_day_hour_td  = []
	for i in range(7):
		sum_day_hour_td.append([timedelta(0)]*24)
	count_day_hour = []
	for i in range(7):
		count_day_hour.append([0]*24)
	
	for call in calls:
		count_day_hour[call.callstart.weekday()][call.callstart.hour] += 1
		if call.callanswered == None:
			sum_day_hour_td[call.callstart.weekday()][call.callstart.hour] += call.callend - call.callstart
		else:
			sum_day_hour_td[call.callstart.weekday()][call.callstart.hour] += call.callanswered - call.callstart
	
	if not retMinutes:
		return sum_day_hour_td, count_day_hour
	
	sum_day_hour_m = []
	for i in range(7):
		sum_day_hour_m.append([0]*24)
	for i in range(7):
		for j in range(24):
			sum_day_hour_m[i][j] = sum_day_hour_td[i][j].seconds / float(60) 
	return sum_day_hour_m, count_day_hour


# returns tuple: (7 lists of 24 timedeltas/minutes, 7 lists of 24 counts)
# excludes active calls and currently waiting
def sum_serv_by_day_hour(company_id, retMinutes):
		calls = Call.objects.filter(company_id=company_id, callstart__isnull=False, callend__isnull=False)
		if len(calls) == 0:
				return None, None
		
		sum_day_hour_td = []
		for i in range(7):
				sum_day_hour_td.append([timedelta(0)]*24)
		count_day_hour = []
		for i in range(7):
				count_day_hour.append([0]*24)
		
		for call in calls:
				count_day_hour[call.callstart.weekday()][call.callstart.hour] += 1
				if call.callanswered != None:
						sum_day_hour_td[call.callstart.weekday()][call.callstart.hour] += call.callend - call.callanswered
		
		if not retMinutes:
				return sum_day_hour_td, count_day_hour
		
		sum_day_hour_m = []
		for i in range(7):
				sum_day_hour_m.append([0]*24)
		for i in range(7):
				for j in range(24):
						sum_day_hour_m[i][j] = sum_day_hour_td[i][j].seconds / float(60)
		return sum_day_hour_m, count_day_hour

