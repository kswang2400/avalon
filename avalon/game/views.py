from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader

from game.models import AvalonUserCreationForm
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
    game = AvalonGame(num_players=7)
    inline_template = """
        num_players: {num_players}<br>
        num_resistance: {num_resistance}<br>
        num_spies: {num_spies}<br>
        mission_sizes: {mission_sizes}<br>
    """.format(
            num_players=game.num_players,
            num_resistance=game.num_resistance,
            num_spies=game.num_spies,
            mission_sizes=game.mission_sizes,
        )

    return HttpResponse(inline_template)