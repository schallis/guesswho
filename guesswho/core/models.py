import logging

from django.db import models

log = logging.getLogger(__name__)


def random_person():  # pragma: no cover
    return Person.objects.order_by('?')[0]


def all_people():  # pragma: no cover
    return Person.objects.all()


class Person(models.Model):
    """The primary actor in the game, collectively a pool of candidates"""
    name = models.CharField(max_length=50)

    def __unicode__(self):  # pragma: no cover
        return self.name


class Player(models.Model):
    """Records the game state for a particular player"""
    user = models.ForeignKey('auth.user')
    person = models.ForeignKey(Person, default=random_person)
    candidates = models.ManyToManyField(Person, related_name="+")

    def __unicode__(self):  # pragma: no cover
        return u'{} (playing as {})'.format(self.user.username,
                                            self.person.name)


class Game(models.Model):
    """Record the state for each game between players"""
    players = models.ManyToManyField(Player)
    start_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    winner = models.ForeignKey(Player, blank=True, null=True,
                               related_name='winning_games')

    def __unicode__(self):  # pragma: no cover
        players = self.players.values_list('user__username', flat=True)
        return u'Game between players: {}'.format(', '.join(players))

    @property
    def player1(self):
        return self.players.order_by('pk')[0]

    @property
    def player2(self):
        return self.players.order_by('pk')[1]


class TraitValue(models.Model):
    """Possible values for each attribute"""
    label = models.CharField(max_length=50)

    def __unicode__(self):  # pragma: no cover
        return u'{} ({})'.format(self.label, self.pk)


class Trait(models.Model):
    """An attribute about a person"""
    name = models.CharField(max_length=50)
    values = models.ManyToManyField(TraitValue)
    question = models.CharField(max_length=255)

    def __unicode__(self):  # pragma: no cover
        return self.name


class PersonTrait(models.Model):
    """Records the attributes for each person"""
    person = models.ForeignKey(Person)
    trait = models.ForeignKey(Trait)
    value = models.ForeignKey(TraitValue)

    def __unicode__(self):  # pragma: no cover
        return '{}: {}'.format(self.trait.name, self.value.label)

    class Meta:
        unique_together = [('person', 'trait')]


class Question(models.Model):
    """Each player will ask question to reduce their pool of candidates"""
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    trait = models.ForeignKey(Trait, related_name='+')
    value = models.ForeignKey(TraitValue)

    class Meta:
        unique_together = [('game', 'player', 'trait', 'value')]
