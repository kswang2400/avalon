from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader

from game.models import AvalonUser, AvalonUserCreationForm
from game.avalon import AvalonGame

def index(request):
    return render(request, 'index.html', {'foo': 'bar'})

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

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


def test_game(request):
    # KW: TODO need to seed users
    fake_users = [
        AvalonUser.objects.get(username='kevin'),
        AvalonUser.objects.get(username='evan'),
        AvalonUser.objects.get(username='choi'),
        AvalonUser.objects.get(username='kent'),
        AvalonUser.objects.get(username='marcus'),
        AvalonUser.objects.get(username='greg'),
    ]

    game = AvalonGame(users=fake_users)

    return HttpResponse(game.print_debug_text())