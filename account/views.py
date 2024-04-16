from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .decorators import check_auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

@check_auth
def register_librarian(request):
    if request.method == "GET":
        unbounded_form = UserCreationForm()
        return render(request,'account/register.html',context={'form':unbounded_form})
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
        else:
            return render(request,'account/register.html',context={'form':form})

@check_auth
def login_view(request):
    if request.method == "GET":
        return render(request,'account/login.html')
    elif request.method == "POST":
        user_name = request.POST.get('username','')
        pass_word = request.POST.get('password','')
        u = authenticate(request,username=user_name,password=pass_word)
        if u is not None:
            login(request,u)
            return HttpResponseRedirect(reverse("account:home"))
        else:
            return render(request,'account/login.html',context={'message':'Invalid credentials'})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("account:login"))

@login_required(login_url='account:login')
def librarian_home(request):
    return render(request,'account/librarian_home.html')


