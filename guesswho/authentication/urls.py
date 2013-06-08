from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from guesswho.authentication.views import login_view


urlpatterns = (
    url(r'^$', login_view, name='login'),
)
