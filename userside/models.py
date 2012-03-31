<<<<<<< HEAD
from django.db import models

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
	phone_number = models.IntegerField()
	
	def __unicode__(self):
		return str(self.phone_number)

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
	rep = models.ForeignKey(Representative)
	callstart = models.DateField(blank=True)
	callanswered = models.DateField(blank=True)
	callend = models.DateField(blank=True)
	
	#Probably want a function like is_active() or something
	
	def __unicode__(self):
		return str(self.id)


	

# Create your models here.
=======
from django.db import models

class Company(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=1000)
	logo_filepath = models.CharField(max_length = 100)
	website_link = models.CharField(max_length = 100)
	
	
class Customer(models.Model):
	phone_number = models.IntegerField()

class CallCenter(models.Model):
	name = models.CharField(max_length = 100)
	location = models.CharField(max_length = 100)

class Representative(models.Model):
	company = models.ForeignKey(Company)
	callcenter = models.ForeignKey(CallCenter)
	first_name = models.CharField(max_length = 20)
	last_name = models.CharField(max_length = 20)
	internal_id = models.CharField(max_length = 100)

class Call(models.Model):
	customer = models.ForeignKey(Customer)
	company = models.ForeignKey(Company)
	rep = models.ForeignKey(Representative)
	callstart = models.DateField()
	callanswered = models.DateField()
	callend = models.DateField()


	

# Create your models here.
>>>>>>> origin/master
