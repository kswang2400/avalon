from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse(
        "Hello, {user}. You're at the polls index.".format(user=request.user))

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    return HttpResponse("Please login first")
