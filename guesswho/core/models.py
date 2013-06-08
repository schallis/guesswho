from django.db import models
from django.core.exceptions import ValidationError


class Person(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Game(models.Model):
    player1 = models.ForeignKey('auth.user', related_name='+')
    player2 = models.ForeignKey('auth.user', related_name='+',
            blank=True, null=True)
    player1_person = models.ForeignKey(Person, related_name='+')
    player2_person = models.ForeignKey(Person, related_name='+')
    player1_candidates = models.ManyToManyField(Person, related_name='+')
    player2_candidates = models.ManyToManyField(Person)
    start_date = models.DateTimeField(blank=True, null=True)
    complete = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Between {} and {}'.format(self.player1,
                                          self.player2 or 'Nobody')

    def save(self, *args, **kwargs):
        """Ensure players are not the same person"""
        if self.player1 == self.player2:
            raise ValidationError('Players cannot play themselves')
        super(Game, self).save(*args, **kwargs)


class TraitValue(models.Model):
    label = models.CharField(max_length=50)

    def __unicode__(self):
        return self.label


class Trait(models.Model):
    name = models.CharField(max_length=50)
    values = models.ManyToManyField(TraitValue)
    question = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class PersonTrait(models.Model):
    person = models.ForeignKey(Person)
    trait = models.ForeignKey(Trait)
    value = models.ForeignKey(TraitValue)

    class Meta:
        unique_together = [('person', 'trait')]


class Question(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey('auth.User')
    trait = models.ForeignKey(Trait, related_name='+')
    value = models.ForeignKey(TraitValue)

    class Meta:
        unique_together = [('game', 'player', 'trait', 'value')]
