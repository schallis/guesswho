from django.views.generic import ListView
from django.shortcuts import render_to_response
from django.template import RequestContext

from guesswho.core.models import Game, Question, Trait, TraitValue
from guesswho.core.logic import (get_game_opponent, is_game_complete,
        rule_out_candidates)
from guesswho.core.forms import QuestionForm


class ListGames(ListView):
    template_name = "core/list_games.html"

    def get_queryset(self):
        return Game.objects.filter(players__user=self.request.user)


def play_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    player = game.players.get(user=request.user)

    candidates = player.candidates.all()
    ctx = {
        'opponent': get_game_opponent(game, player),
        'person': player.person,
        'num_candidates': candidates.count(),
        'candidates': candidates
    }

    if request.method == 'POST':
        form = QuestionForm(game, player, request.POST)
        if form.is_valid():
            custom_key = form.cleaned_data.get('question')
            trait_id, value_id = custom_key.split(':')
            question_data = {
                'game': game,
                'player': player,
                'trait': Trait.objects.get(pk=trait_id),
                'value': TraitValue.objects.get(pk=value_id)
            }
            question = Question(**question_data)
            rule_out_candidates(question)
            winner = is_game_complete(game)
            if winner:
                ctx.update({
                    'game_over': True,
                    'user_won': winner.pk is player.pk
                })
    else:
        form = QuestionForm(game, player)
    ctx['form'] = form

    return render_to_response('core/play_game.html', ctx,
                              context_instance=RequestContext(request))
