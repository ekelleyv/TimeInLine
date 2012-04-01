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
	