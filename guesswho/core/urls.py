from django.conf.urls import patterns, include, url

from guesswho.core.views import ListGames, play_game


urlpatterns = (
    url(r'^game/$', ListGames.as_view(), name='list_games'),
    url(r'^game/new/$', ListGames.as_view(), name='new_game'),
    url(r'^game/join/(?P<game_id>\d)$', ListGames.as_view(), name='join_game'),
    url(r'^game/(?P<game_id>\d)', play_game, name='play_game'),
)
