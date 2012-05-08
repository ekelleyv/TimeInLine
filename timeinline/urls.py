from django.conf.urls import patterns, include, url
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	url(r'^$', 'userside.views.splash', name='splash'),
	url(r'^dashboard/$', 'userside.views.dashboard', name='dashboard'),
	url(r'^review/$', 'userside.views.review', name='review'),
	
	#Display Calls:
	url(r'^callslist$', 'userside.views.callslist', name='callslist'),
	
	#Test Calls:
	url(r'^test$', 'userside.views.testcalls', name='testcalls'),
	
	#API CALLS
	#url.com/api/call/company_id/caller_id
	url(r'^api/call/(?P<company_id>\d+)/(?P<caller_id>\d+)/$', 'userside.views.call_api'),
	
	#url.com/api/pickup/company_id/rep_id/caller_id
	url(r'^api/pickup/(?P<company_id>\d+)/(?P<rep_id>\d+)/(?P<caller_id>\d+)/$', 'userside.views.pickup_api'),
	
	#url.com/api/hangup/company_id/caller_id
	url(r'^api/hangup/(?P<company_id>\d+)/(?P<caller_id>\d+)/$', 'userside.views.hangup_api'),
	
	# url(r'^timeinline/', include('timeinline.foo.urls')),
	
	#TEST URLS
	#url.com/api/hangup/company_id/caller_id
	#View active calls
	url(r'^test/active/(?P<company_id>\d+)$', 'userside.views.test_active_calls'),
	
	#View position in line
	url(r'^test/position/(?P<company_id>\d+)/(?P<caller_id>\d+)$', 'userside.views.test_position'),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),

	# catch everything else
	#url(r'^', 'userside.views.misc', name='misc'),
)
