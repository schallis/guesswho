from django import forms

from guesswho.core.models import Question, Trait


def get_questions(game):
    """Display selection of questions based on traits

    We're using a custom key here to retrieve both the trait and value IDs in a
    single input
    """
    choices = []
    for trait in Trait.objects.all():
        for choice in trait.values.all():
            label = trait.question.format(choice.label)
            custom_key = '{}:{}'.format(trait.pk, choice.pk)
            choices.append((custom_key, label))

    return choices


class QuestionForm(forms.ModelForm):

    def __init__(self, player, game, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['question'] = forms.ChoiceField(choices=get_questions(game))

    class Meta:
        model = Question
        fields = []
