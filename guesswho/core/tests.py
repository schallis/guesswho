from mock import Mock
from nose.tools import assert_raises

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from guesswho.core.models import Person, Game


def test_players_cannot_play_self():
    player = User.objects.get(pk=1)
    person = Person.objects.get(pk=1)
    with assert_raises(ValidationError):
        Game(player1=player, player2=player,
             player1_person=person, player2_person=person).save()


def test_players_can_play_others():
    player1 = User.objects.get(pk=1)
    player2 = User.objects.get(pk=2)
    person = Person.objects.get(pk=1)
    Game(player1=player1, player2=player2,
         player1_person=person, player2_person=person).save()
