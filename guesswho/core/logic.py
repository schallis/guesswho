def is_game_complete()
    # Check player 1
    Guess.objects.all
    for guess in guesses:
        Q(guess.trait.name, guess.trait.value)
    Person.objects.filter()


def reduce_candidates(candidates, question):
   """Reduce the possible list of candidates based on the question"""
   qfilters = []
   if question_correct(question, player1_person):
       qfilters.append(~Q(question))

   return remaining.filter(qfilters)


def question_correct(question):
    question.game




def get_question_target(question):
    """Get the game user who is not the one that asked the question"""
    if question.game.player1 != question.player:
        return question.game.player2
    return question.game.player1
