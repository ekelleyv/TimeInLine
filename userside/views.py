# Create your views here.
from django.template import Context, loader
from userside.models import *
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone


def splash(request):
	calls = Call.objects.all()
	t = loader.get_template('index.html')
	c = Context({'calls':calls})
	return HttpResponse(t.render(c))
	
def dashboard(request, caller_id):
	return HttpResponse("Hello " + caller_id)

def call_api(request, company_id, caller_id):
	#Check if customer exists
	try:
		customer = Customer.objects.get(phone_number = caller_id)
	#Create new customer
	except Customer.DoesNotExist:
		customer = Customer(phone_number = caller_id)
		customer.save()
		
	#Check if company exists
	try:
		company = Company.objects.get(id = company_id)
	#This should not happen, exit
	except Company.DoesNotExist:
		return HttpResponse("Company " + company_id + " does not exist.")
	
	#Create new call
	call = Call(callstart = timezone.now(), customer=customer, company=company)
	call.save()
	return HttpResponse("Call at " + str(call.callstart))

def pickup_api(request, company_id, rep_id, caller_id):
	#Check if customer exists
	try:
		customer = Customer.objects.get(phone_number = caller_id)
	#This should not happen, exit
	except Customer.DoesNotExist:
		return HttpResponse("Customer " + caller_id + " does not exist.")
		
	#Check if company exists
	try:
		company = Company.objects.get(id = company_id)
	#This should not happen, exit
	except Company.DoesNotExist:
		return HttpResponse("Company " + company_id + " does not exist.")
		
	#Check if representative exists
	try:
		rep = Representative.objects.get(internal_id = rep_id)
	#This should not happen, exit
	except Representative.DoesNotExist:
		return HttpResponse("Rep " + rep_id + " does not exist.")
	
	#Try and get the most recent call
	try:
		call = Call.objects.filter(customer = customer).order_by('-callstart')[0] #FIRST OR LAST??
	#This should not happen
	except Call.DoesNotExist:
		return HttpResponse("Call " + caller_id + " does not exist.")
	
	if (call.callend):
		return HttpResponse("There is no active call")
	if (call.callanswered):
		return HttpResponse("The call was already picked up")
	call.rep = rep
	call.callanswered = timezone.now()
	call.save()
	return HttpResponse("Call picked up at " + str(call.callanswered))

def hangup_api(request, company_id, caller_id):
	#Check if customer exists
	try:
		customer = Customer.objects.get(phone_number = caller_id)
	#This should not happen, exit
	except Customer.DoesNotExist:
		return HttpResponse("Customer " + caller_id + " does not exist.")
		
	#Check if company exists
	try:
		company = Company.objects.get(id = company_id)
	#This should not happen, exit
	except Company.DoesNotExist:
		return HttpResponse("Company " + company_id + " does not exist.")
	
	#Try and get the most recent call
	try:
		call = Call.objects.filter(customer = customer).order_by('-callstart')[0] #FIRST OR LAST??
	#This should not happen
	except Call.DoesNotExist:
		return HttpResponse("Call " + caller_id + " does not exist.")
	
	if (call.callend):
		return HttpResponse("Call already ended")
	
	call.callend = timezone.now()
	call.save()
	return HttpResponse("Call ended at " + str(call.callend))
	
