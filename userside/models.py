from django.db import models
from django.utils import timezone

class Company(models.Model):
	#add this so that in the admin it is 'companies' not 'companys'
	class Meta:
		verbose_name_plural = "companies"
	
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=1000, blank=True)
	logo_filepath = models.CharField(max_length = 100, blank=True)
	website_link = models.CharField(max_length = 100, blank=True)
	
	def __unicode__(self):
		return self.name
	
	
class Customer(models.Model):
	phone_number = models.CharField(max_length=20)
	
	def __unicode__(self):
		return self.phone_number

class CallCenter(models.Model):
	company = models.ForeignKey(Company)
	name = models.CharField(max_length = 100)
	location = models.CharField(max_length = 100, blank=True)
	description = models.CharField(max_length = 1000, blank=True)
	
	def __unicode__(self):
		return self.name

class Representative(models.Model):
	company = models.ForeignKey(Company)
	callcenter = models.ForeignKey(CallCenter, blank=True)
	first_name = models.CharField(max_length = 20, blank=True)
	last_name = models.CharField(max_length = 20, blank=True)
	internal_id = models.CharField(max_length = 100)
	
	def __unicode__(self):
		return self.internal_id

class Call(models.Model):
	customer = models.ForeignKey(Customer)
	company = models.ForeignKey(Company)
	rep = models.ForeignKey(Representative, null=True)
	callstart = models.DateTimeField(null=True)
	callanswered = models.DateTimeField(null=True)
	callend = models.DateTimeField(null=True)
	
	#Probably want a function like is_active() or something
	
	def __unicode__(self):
		return str(self.id)
		
class Review(models.Model):
	call = models.ForeignKey(Call)
	overall_rating = models.IntegerField()
	rep_rating = models.IntegerField()
	waiting_rating = models.IntegerField()
	comments = description = models.CharField(max_length = 10000, blank=True)


	

# Create your models here.
