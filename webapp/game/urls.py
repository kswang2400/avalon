from django.conf.urls import url
from django.contrib.auth import views as auth_views

from game import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^game/new/$', views.new_game, name='new_game'),
    url(r'^game/([0-9]*)/$', views.game, name='game'),
    url(r'^quest/finalize/$', views.finalize_quest, name='finalize_quest'),
    url(r'^vote/quest/$', views.vote_on_quest, name='vote_on_quest'),
    url(r'^vote/for_quest/$', views.vote_for_quest, name='vote_for_quest'),
    url(r'^suggest/$', views.questmaster_suggest, name='questmaster_suggest'),
    url(r'^finalize_vote_for_quests/$', views.finalize_vote_for_quests, name='finalize_vote_for_quests'),
]