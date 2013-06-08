from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from guesswho.core.views import (ListGames, create_game, join_game, play_game)


urlpatterns = patterns('',
    url(r'^game/$', login_required(ListGames.as_view()), name='list_games'),
    url(r'^game/new/$', login_required(create_game), name='new_game'),
    url(r'^game/to_join/$', login_required(join_game), name='games_to_join'),
    url(r'^game/join/(?P<game_id>\d+)$', login_required(ListGames.as_view()), name='join_game'),
    url(r'^game/(?P<game_id>\d+)', login_required(play_game), name='play_game'),
)
