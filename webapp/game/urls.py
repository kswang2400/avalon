from django.conf.urls import url
from django.contrib.auth import views as auth_views

from game import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    # KW: TODO better game pk parsing
    url(r'^game/([0-9])/$', views.game, name='game'),
    url(r'^suggest/$', views.questmaster_suggest, name='questmaster_suggest'),
    url(r'^mock_vote_for_quest/$', views.mock_vote_for_quest, name='mock_vote_for_quest'),
]