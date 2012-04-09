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
	