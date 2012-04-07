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
		response.write("Comparing call " + str(call.id) + " against " + str(current_call.id) + "<br>")
		if (call.callstart < current_call.callstart):
			response.write("Smaller")
			count = count + 1
	response.write("Count = " + str(count))
	return response

# excludes active calls and currently waiting
def avg_wait(company):
  calls = Call.objects.filter(company_id=company, callstart__isnull=False, callend__isnull=False)
  if len(calls) == 0:
    return 0
  else:
    deltasum = datetime.timedelta(0)
    for call in calls:
      if call.answered == None:
	deltasum += call.callend - call.callstart
      else:
	deltasum += call.callanswered - call.callstart
    avg_timedelta = deltasum / len(calls)
    return avg_timedelta

# returns list of timedeltas for hours 0-23
def avg_wait_by_hour(company):
  calls = Call.objects.filter(company_id=company, callstart__isnull=False, callend__isnull=False)
  deltasum_hour = [datetime.timedelta(0)]*24
  count_hour = [0]*24
  for call in calls:
    count_hour[call.callstart.hour] += 1
    if call.answered == None:
      deltasum_hour[call.callstart.hour] += call.callend - call.callstart
    else:
      deltasum_hour[call.callstart.hour] += call.callanswered - call.callstart
  delta_avg_hour = [datetime.timedelta(0)]*24
  for i in range(24):
    delta_avg_hour[i] = deltasum_hour[i] / count_hour[i]
    # convert to minutes? seconds? (total_second() in python 2.7)
  return avg_delta_hour

# returns list of timedeltas for days 0-6
def avg_wait_by_day(company):
  calls = Call.objects.filter(company_id=company, callstart__isnull=False, callend__isnull=False)
  deltasum_day = [datetime.timedelta(0)]*7
  count_day = [0]*7
  for call in calls:
    count_day[call.callstart.day] += 1
    if call.callanswered == None:
      deltasum_day[call.callstart.day] += call.callend - call.callstart
    else:
      deltasum_day[call.callstart.day] += call.callanswered - call.callstart
  delta_avg_day = [datetime.timedelta(0)]*7
  for i in range(7):
    delta_avg_day[i] = deltasum_day[i] / count_day[i]
  return delta_avg_day

# returns 7 lists of 24 timedeltas
def avg_wait_by_day_hour(company):
  calls = Call.objects.filter(company_id=company, callstart__isnull=False, callend__isnull=False)
  deltasum_day_hour = [ [datetime.timedelta(0)*24] ]*7
  count_day_hour = [ [0]*24 ]*7
  for call in calls:
    count_day_hour[call.callstart.day][call.callstart.hour] += 1
    if call.callanswered == None:
      deltasum_day_hour[call.callstart.day][call.callstart.hour] += call.callend - call.callstart
    else:
      deltasum_day_hour[call.callstart.day][call.callstart.hour] += call.callanswered - call.callstart
  delta_avg_day_hour = [ [datetime.timedelta(0)*24] ]*7
  for i in range(7):
    for j in range(24):
      delta_avg_day_hour[i][j] = deltasum_day_hour[i][j] / count_day_hour[i][j]
  return delta_avg_day_hour




