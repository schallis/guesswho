from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from guesswho.authentication.views import login_view


urlpatterns = patterns('',
    url(r'^$', login_view, name='login'),
)
