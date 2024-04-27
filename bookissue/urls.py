from .views import *
from django.urls import path
app_name='bookissue'
urlpatterns = [
    path('issuebook',issue_book,name='issuebook'),
    path('return',return_book,name='return'),
    path('',index,name="index"),
    path('view/<int:bookissueid>',view,name='view_bookissue')
]
