from django.db import models

# Create your models here.
class Book(models.Model):
    book_id = models.CharField(max_length=15,null=False,blank=False,unique=True)
    title = models.CharField(max_length=100,null=False)
    author = models.CharField(max_length=50,null=False)

