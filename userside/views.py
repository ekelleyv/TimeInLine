# Create your views here.
from django.template import Context, loader
from userside.models import *
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from datetime import datetime
from django.utils import timezone, simplejson
from userside.stats import *

def test_active_calls(request, company_id):
	calls = active_calls(company_id)
	#calls = Call.objects.all()
	t = loader.get_template('test/index.html')
	c = Context({'calls':calls})
	return HttpResponse(t.render(c))

def test_position(request, company_id, caller_id):
	return place_in_line(company_id, caller_id)
	
def splash(request):
	t = loader.get_template('bootstrap.html')
	c = Context()
	return HttpResponse(t.render(c))
	
def callslist(request):
	calls = Call.objects.all()
	t = loader.get_template('callslist.html')
	c = Context({'calls':calls})
	return HttpResponse(t.render(c))
	
def testcalls(request):
	t = loader.get_template('test.html')
	c = Context()
	return HttpResponse(t.render(c))
	
def dashboard(request):
	caller_id = request.GET.get('caller_id')
	xhr = request.GET.has_key('xhr')
	response_dict = {}
	try:
		customer = Customer.objects.get(phone_number = caller_id)
	#Create new customer
	except Customer.DoesNotExist:
		return HttpResponseNotFound('<h1>Page not found</h1>')
	
	
	company = active_company(caller_id)
	position = place_in_line(company, caller_id)
	response_dict.update({'position':position})
	
	if xhr:
		return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
	
	return render_to_response('bootstrap-dashboard.html', response_dict);

def call_api(request, company_id, caller_id):
	
	
	#Check if customer exists
	try:
		customer = Customer.objects.get(phone_number = caller_id)
	#Create new customer
	except Customer.DoesNotExist:
		customer = Customer(phone_number = caller_id)
		customer.save()
	
	prev_calls = Call.objects.filter(customer = customer).order_by('-callstart')

	if (len(prev_calls) > 0):
		if (not prev_calls[0].callend):
			return HttpResponse("There is already an active call from this number")
	
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
	
	if(call.callend):
		return HttpResponse("Call already picked up")
	if(call.callend):
		return HttpResponse("Call already ended")			

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
	
