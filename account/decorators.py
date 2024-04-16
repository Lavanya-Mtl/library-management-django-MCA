from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def check_auth(myfunc):
    def inner(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("account:home"))
        else:
            return myfunc(request)
    return inner
        