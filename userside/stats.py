from userside.models import *
from django.http import HttpResponse
from datetime import datetime

#Returns all of the active calls for a given company
def active_calls(company):
	calls = Call.objects.filter(company_id = company, callanswered__isnull=True, callend__isnull=True)
	return calls

def place_in_line(company, caller_id):
	response = HttpResponse()
	customer = Customer.objects.get(phone_number = caller_id)
	calls = active_calls(company)
	current_call = Call.objects.filter(customer = customer).order_by('-callstart')[0]
	count = 1
	for call in calls:
		if (call.callstart < current_call.callstart):
			count = count + 1
	return count

def active_company(caller_id):
	curr_customer = Customer.objects.get(phone_number = caller_id)
	call = Call.objects.filter(customer = curr_customer, callanswered__isnull=True, callend__isnull=True)[0]
	return call.company

# returns timedelta/minutes
def avg_wait(company, retMinutes):
  sums, counts = sum_wait_by_day_hour(company, retMinutes)
  if sums is None:
    return None
  sum = 0 if retMinutes else datetime.timedelta(0)
  count = 0
  for i in range(7):
    for j in range(24):
      sum += sums[i][j]
      count += counts[i][j]
  return sum / count

# return list (0-7) of timedeltas/minutes
def avg_wait_by_hour(company, retMinutes):
  sums, counts = sum_wait_by_day_hour(company, retMinutes)
  if sums is None:
    return None
  avg_hour = [0]*24 if retMinutes else [datetime.timedelta(0)]*24
  for j in range(24):
    sum = 0 if retMinutes else datetime.timedelta(0)
    count = 0
    for i in range(7):
      sum += sums[i][j]
      count += counts[i][j]
    avg_hour[j] = sum / count
  return avg_hour

# return list (0-6) of timedeltas/minutes
def avg_wait_by_day(company, retMinutes):
  sums, counts = sum_wait_by_day_hour(company, retMinutes)
  if sums is None:
    return None
  avg_day = [0]*7 if retMinutes else [datetime.timedelta(0)]*7
  for i in range(7):
    sum = 0 if retMinutes else datetime.timedelta(0)
    count = 0
    for j in range(24):
      sum += sums[i][j]
      count += counts[i][j]
    avg_day[i] = sum / count
  return avg_day

# return 7 lists of 24 timedeltas/minutes
def avg_wait_by_day_hour(company, retMinutes):
  sums, counts = sum_wait_by_day_hour(company, retMinutes)
  if sums is None:
    return None
  avg_day_hour = [ [0]*24 ]*7 if retMinutes else [ [datetime.timedelta(0)]*24 ]*7
  for i in range(7):
    for j in range(24):
      avg_day_hour[i][j] = sums[i][j] / counts[i][j]
  return avg_day_hour

# returns tuple: (7 lists of 24 timedeltas/minutes, 7 lists of 24 counts)
# excludes active calls and currently waiting
def sum_wait_by_day_hour(company, retMinutes):
  calls = Call.objects.filter(company_id=company, callstart__isnull=False, callend__isnull=False)
  if len(calls) == 0:
    return None, None

  sum_day_hour_td = [ [datetime.timedelta(0)]*24 ]*7
  count_day_hour = [ [0]*24 ]*7
  for call in calls:
    count_day_hour[call.callstart.day][call.callstart.hour] += 1
    if call.callanswered == None:
      deltasum_day_hour[call.callstart.day][call.callstart.hour] += call.callend - call.callstart
    else:
      deltasum_day_hour[call.callstart.day][call.callstart.hour] += call.callanswered - call.callstart
 
  if not retMinutes:
    return sum_day_hour_td, count_day_hour

  avg_day_hour_m = [ [0]*24 ]*7
  for i in range(7):
    for j in range(24):
      avg_day_hour_m[i][j] = d.seconds / float(60) 
  return avg_day_hour_m, count_day_hour








