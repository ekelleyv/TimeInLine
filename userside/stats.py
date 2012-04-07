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

def avg_wait(company):
  # excludes active calls and currently waiting
  calls = Call.objects.filter(company_id=company, callstart__isnull=False, callend__isnull=False)
  if len(calls) == 0:
    return 0
  else:
    #timedeltas = []
    deltasum = datetime.timedelta(0)
    for call in calls:
      if call.answered == None:
	#timedeltas.append(call.callend - call.callstart)
	deltasum += call.callend - call.callstart
      else:
	#timedeltas.append(call.callanswered - call.callstart)
	deltasum += call.callanswered - call.callstart
    # stackoverflow: giving datetime.timedelta(0) as the start value makes sum work on timedeltas
    #avg_timedelta = sum(timedeltas, datetime.timedelta(0)) / len(timedeltas)
    avg_timedelta = deltasum / len(calls)
    return avg_timedelta

# returns list for hours 0-23
def avg_wait_by_hour(company):
  calls = Call.objects.filter(company_id=company, callstart__isnull=False, callend__isnull=False)
  deltasum_hour =
  count_hour =
  for call in calls:
    count_hour[call.day] += 1
    if call.answered == None:
      deltasum_hour[call.day] += call.callend - call.callstart
    else:
      deltasum_hour[call.day] += call.callanswered - call.callstart
  avg_delta_hour = deltasum_hour / count_hour # (element-wise)
  return avg_delta_hour

def avg_wait_by_day(company):
  # fill

def avg_wait_by_day_hour(company):
  # list of 7 lists of size 24
