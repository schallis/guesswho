import logging

from guesswho.core.models import Person
from guesswho.core.exceptions import BadGameConfig

log = logging.getLogger(__name__)


def has_player_won(player):
    candidates_left = player.candidates.count()
    if candidates_left < 1:
        msg = 'No candidates matched the question'
        log.error(msg)
        raise BadGameConfig(msg)
    if candidates_left is 1:
        return True
    return False


def is_game_complete(game):
    for player in [game.player1, game.player2]:
        if has_player_won(player):
            game.completed = True
            game.winner = player
            game.save()
            return player
    return False


def question_as_query(question):
    return {
        'persontrait__trait__name': question.trait.name,
        'persontrait__value': question.value.pk
    }


def question_correct(question):
    """Is the opponents person in the set that matches the question"""
    opponent = get_game_opponent(question.game, question.player)
    query = question_as_query(question)
    if opponent.person in Person.objects.filter(**query):
        return True
    return False


def rule_out_candidates(question):
    """Reduce the possible list of candidates based on the question"""
    correct = question_correct(question)
    query = question_as_query(question)
    if correct:
        # Remove anyone that does not have the traits
        to_remove = question.player.candidates.exclude(**query)
    else:
        # Remove anyone that has the traits
        to_remove = question.player.candidates.filter(**query)
    question.player.candidates.remove(*to_remove)


def get_game_opponent(game, player):
    """Get the game user who is not the one that asked the question"""
    if game.player1.pk is player.pk:
        return game.player2
    return game.player1
