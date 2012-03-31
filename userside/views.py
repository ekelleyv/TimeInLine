# Create your views here.
from django.template import Context, loader
from userside.models import *
from django.http import HttpResponse


def splash(request):
	customers = Customer.objects.all()
	t = loader.get_template('index.html')
	c = Context({'customers':customers})
	return HttpResponse(t.render(c))
	
def dashboard(request, caller_id):
	return HttpResponse("Hello " + caller_id)

def call_api(request, company_id, caller_id):
	return HttpResponse("Call from " + caller_id + " to " + company_id)

def pickup_api(request, company_id, caller_id):
	return HttpResponse("Call from " + caller_id + " to " + company_id)

def hangup_api(request, company_id, caller_id):
	return HttpResponse("Call from " + caller_id + " to " + company_id)
	