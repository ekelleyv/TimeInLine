import string
import random
import userside.models

def keyGen(length=10):
    letters = string.ascii_letters + string.digits
    while True:
        new_key = ''.join([random.choice(letters) for _ in range(length)])
        if not userside.models.Company.objects.filter(key=new_key):
            return new_key