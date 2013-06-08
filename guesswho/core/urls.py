from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from guesswho.core.views import ListGames, play_game


urlpatterns = (
    url(r'^game/$', login_required(ListGames.as_view()), name='list_games'),
    url(r'^game/new/$', login_required(ListGames.as_view()), name='new_game'),
    url(r'^game/join/(?P<game_id>\d)$', login_required(ListGames.as_view()), name='join_game'),
    url(r'^game/(?P<game_id>\d)', login_required(play_game), name='play_game'),
)

