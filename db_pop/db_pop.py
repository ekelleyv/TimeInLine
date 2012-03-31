from django.core.management import setup_environ
from timeinline import settings
from userside.models import *

setup_environ(settings)

co1 = Company(name='Apple')
co1.save()

