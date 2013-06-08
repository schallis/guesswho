from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from guesswho.authentication.forms import LoginForm
from guesswho.authentication.utils import log_user_in_without_password


def login_view(request):
    """A simple password-less login page"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('player_name')
            user, __ = auth.models.User.objects.get_or_create(username=name)
            log_user_in_without_password(request, user)
            return HttpResponseRedirect(reverse('list_games'))
    else:
        form = LoginForm()
    ctx = {
        "form": form
    }

    return render_to_response('authentication/login.html', ctx,
                              context_instance=RequestContext(request))
