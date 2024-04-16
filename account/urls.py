from django.urls import path
from .views import *
app_name='account'
urlpatterns = [
     path('login',login_view,name="login"),
     path('logout',logout_view,name="logout"),
     path('home',librarian_home,name="home"),
     path('register',register_librarian,name="register"),
]
 