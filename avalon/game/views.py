from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from game.models import AvalonUserCreationForm

def index(request):
    return HttpResponse(
        "Hello, {user}. You're at the polls index.".format(user=request.user))


def signup(request):
    if request.method == 'POST':
        form = AvalonUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('index')
    else:
        form = AvalonUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    template = loader.get_template('login.html')
    context = {
        'foo': 'bar',
    }

    return HttpResponse(template.render(context, request))
