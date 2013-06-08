"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from mock import patch
from nose.tools import eq_

from django.test import TestCase
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class LoginTest(TestCase):
    def test_login_enforce(self):
        response = self.client.get(reverse('list_games'))

        self.assertTrue(isinstance(response, HttpResponseRedirect))
        eq_(response['location'], 'http://testserver/?next=/game/')

    @patch('guesswho.authentication.utils.auth')
    def test_login_page(self, auth):
        data = {
            "player_name": "Steve"
        }
        response = self.client.post(reverse('login'), data, follow=True)

        eq_(auth.login.call_count, 1)
        eq_(response.status_code, 200)

    @patch('guesswho.authentication.utils.auth')
    def test_login_page_failure(self, auth):
        data = {}
        response = self.client.post(reverse('login'), data, follow=True)

        form_error = {'player_name': [u'This field is required.']}
        eq_(response.context['form']._errors, form_error)
        eq_(auth.login.call_count, 0)
        eq_(response.status_code, 200)
