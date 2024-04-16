from django.db import models

# Create your models here.

class Member(models.Model):
    username = models.CharField(max_length=40,unique=True,null=False,blank=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(null=False,blank=False)
    phone_number = models.CharField(max_length=15)
    dues = models.IntegerField(null=False,default=0)
