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
