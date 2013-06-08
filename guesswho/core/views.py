from django.views.generic import ListView, CreateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Count

from guesswho.core.models import (Game, Question, Trait, TraitValue, Player,
        all_people)
from guesswho.core.logic import (get_game_opponent, is_game_complete,
        rule_out_candidates)
from guesswho.core.forms import QuestionForm


class ListGames(ListView):
    template_name = "core/list_games.html"

    def get_queryset(self):
        return Game.objects.filter(players__user=self.request.user)


def create_game(request):
    game = Game.objects.create()
    player1 = Player.objects.create(user=request.user)
    player1.candidates.add(*all_people())
    game.players.add(player1)
    game.save()
    return HttpResponseRedirect(reverse('games_to_join'))


def join_game(request):
    ctx = {
        'games': Game.objects.annotate(player_count=Count('players'))
                    .filter(player_count=1)
    }

    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        game = Game.objects.get(pk=int(game_id))
        player2 = Player.objects.create(user=request.user)
        player2.candidates.add(*all_people())
        game.players.add(player2)
        game.save()
        return HttpResponseRedirect(reverse('play_game', args=(game.pk,)))

    return render_to_response('core/games_to_join.html', ctx,
                              context_instance=RequestContext(request))



def play_game(request, game_id):
    game = Game.objects.get(pk=int(game_id))
    player = game.players.filter(user=request.user)[0]

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
