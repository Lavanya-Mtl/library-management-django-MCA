from django.db import models

from books.models import Book
from members.models import Member

# Create your models here.

class BookIssue(models.Model):
    book = models.OneToOneField(Book,on_delete=models.RESTRICT,null=False,blank=False)
    member = models.OneToOneField(Member,on_delete=models.RESTRICT,null=False,blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    for_days = models.IntegerField(default=7,null=False,blank=True)
