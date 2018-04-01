from django.conf import settings
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader

from game.forms import AvalonUserCreationForm
from game.avalon import Game

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

def game(request, pk):
    debug = request.GET.get('debug') == 'true' or settings.DEBUG
    game = Game(pk=pk)

    return render(request, 'game.html', game.get_debug_context(debug=debug))

def vote_on_quest(request):
    # KW: this should be a POST handler decorator
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('index'))

    user = request.user
    game_pk = int(request.POST.get('game_pk'))
    vote = request.POST.get('vote', 'pass')

    game = Game(pk=game_pk)
    game.game.avalon_game.handle_vote_on_quest(user, vote)

    return HttpResponseRedirect(reverse('game', args=[game.game.pk]))

def mock_vote_for_quest(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('index'))

    # KW: TODO this is for mocking anyways
    # game_pk = int(request.POST.get('game_pk'))

    game = Game(pk=8)
    game.mock_game_user_quest_member_votes()
    game.game.avalon_game.handle_vote_for_quest()

    return HttpResponseRedirect(reverse('game', args=[game.game.pk]))

def questmaster_suggest(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('index'))

    game_pk = int(request.POST.get('game_pk'))
    member_ids = list(map(int, request.POST.getlist('users')))

    game = Game(pk=game_pk)
    game.game.current_quest.reset_members(member_ids)

    return HttpResponseRedirect(reverse('game', args=[game.game.pk]))