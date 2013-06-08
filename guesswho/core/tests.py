from mock import patch, Mock
from nose.tools import assert_raises, eq_

from django.test import TestCase
from django.core.urlresolvers import reverse

from guesswho.core.models import (Game, Question, Trait, TraitValue)
from guesswho.core.logic import (rule_out_candidates, get_game_opponent,
        is_game_complete)
from guesswho.core.exceptions import BadGameConfig


class LogicTests(TestCase):

    fixtures = ['game_logic']

    def test_get_game_opponent_as_1(self):
        game = Game.objects.get(pk=1)
        player = game.player1

        eq_(get_game_opponent(game, player).pk, 2)

    def test_get_game_opponent_as_2(self):
        game = Game.objects.get(pk=1)
        player = game.player2

        eq_(get_game_opponent(game, player).pk, 1)

    def test_rule_out_candidates_question_correct(self):
        game = Game.objects.get(pk=1)
        trait = Trait.objects.get(pk=2)
        trait_value = TraitValue.objects.get(pk=4)
        eq_(game.player2.candidates.count(), 3)

        question = Question(game=game, player=game.player1,
                            trait=trait, value=trait_value)
        rule_out_candidates(question)

        eq_(game.player1.candidates.count(), 1)

    def test_rule_out_candidates_question_not_correct(self):
        game = Game.objects.get(pk=1)
        trait = Trait.objects.get(pk=3)
        trait_value = TraitValue.objects.get(pk=1)
        eq_(game.player2.candidates.count(), 3)

        question = Question(game=game, player=game.player1,
                            trait=trait, value=trait_value)
        rule_out_candidates(question)

        eq_(game.player1.candidates.count(), 3)

    def test_game_over(self):
        game = Game.objects.get(pk=1)
        most_candidates = game.player1.candidates.all()[1:]
        game.player1.candidates.remove(*most_candidates)

        eq_(is_game_complete(game), game.player1)

    def test_game_not_over(self):
        game = Game.objects.get(pk=1)

        eq_(is_game_complete(game), False)

    def test_bad_game_ending(self):
        game = Game.objects.get(pk=1)
        all_candidates = game.player1.candidates.all()
        game.player1.candidates.remove(*all_candidates)

        with assert_raises(BadGameConfig):
            eq_(is_game_complete(game), True)


class TestViews(TestCase):

    fixtures = ['game_logic']

    def setUp(self):
        self.client.login(username='user1', password='admin')

    def test_games_list(self):
        response = self.client.get(reverse('list_games'))

        eq_(response.status_code, 200)
        eq_(response.context['user'].username, 'user1')

    def test_play_get(self):
        response = self.client.get(reverse('play_game', args=(1,)))

        eq_(response.status_code, 200)
        eq_(response.context['user'].username, 'user1')
        eq_(response.context['num_candidates'], 3)

    def test_play_post(self):
        data = {
            'question': '1:1'
        }
        response = self.client.post(reverse('play_game', args=(1,)), data)

        eq_(response.status_code, 200)
        eq_(response.context['user'].username, 'user1')
        eq_(response.context['num_candidates'], 3)

    @patch('guesswho.core.views.is_game_complete')
    def test_play_post_winning(self, complete):
        complete.return_value = Mock(pk=1)
        data = {
            'question': '1:1'
        }
        response = self.client.post(reverse('play_game', args=(1,)), data)

        eq_(response.status_code, 200)
        eq_(response.context['user'].username, 'user1')
        eq_(response.context['user_won'], True)

    @patch('guesswho.core.views.is_game_complete')
    def test_play_post_invalid(self, complete):
        data = {
            'question': 'invalid'
        }
        response = self.client.post(reverse('play_game', args=(1,)), data)

        eq_(response.status_code, 200)
        error = {'question': [u'Select a valid choice. invalid is not ' \
                               'one of the available choices.']}
        eq_(response.context['form']._errors, error)
