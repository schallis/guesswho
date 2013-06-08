from mock import Mock
from nose.tools import assert_raises, eq_

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from guesswho.core.models import (Person, Game, Question, Trait, TraitValue,
        Player)
from guesswho.core.logic import (rule_out_candidates, get_game_opponent,
        is_game_complete)
from guesswho.core.exceptions import BadGameConfig, InvalidQuestion



class ModelTests(TestCase):

    fixtures = ['initial_data']

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

    def test_invalid_question(self):
        game = Game.objects.get(pk=1)
        trait = Trait.objects.get(pk=2)
        trait_value = TraitValue.objects.get(pk=1)
        eq_(game.player2.candidates.count(), 3)

        with assert_raises(InvalidQuestion):
            question = Question(game=game, player=game.player1,
                                trait=trait, value=trait_value)

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


    #def test_players_cannot_play_self(self):
        #game = Game.objects.get(pk=1)
        #game.players.add(game.player1)
