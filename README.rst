Guess Who?
==========
:Info: A Django implementation of the 1979 game [Guess
       Who](http://en.wikipedia.org/wiki/Guess_Who%3F)
:Authors: Steven Challis (http://schallis.com)
:Requires: Python 2.7 (see requirements.txt)

The Brief
=========
Make a website that allows people to play the game Guess Who.

You can define the project pretty much as you like. Play against the computer? Or against others online? Standard deck of cards, or something different? Boolean or multiple outcome questions (eg "is hair blonde" vs "what's colour of hair")? Simple or compound questions (eg "is hair blonde" vs "is either hair blonde or wears glasses")?

* Assume low traffic, eg never more than 5 concurrent players. 
* Don't worry about visual design. Assume it's going to go to a designer and html/css dev after you. 
* Do worry about usability. 
* Write code and unittests as if project were to be handed over to another dev to maintain and extend. 
* You have until midnight (obviously you're not obliged to use all that time) Please ensure code is pushed to Github.

Running tests
=============
The entire test suite can be run by executing the `ci-build.sh` script. This
will also generate linting (`pep8.txt`, `pylint.txt`) and coverage reports
(`htmlcov/index.html`).


TODO:
=====
* Enforce asking questions in turns
* Deplete questions as they get asked
* Prevent more than two players being added to a game
* Prevent the same user joining their own game
* Move view logic to API endpoints and implement Ajax frontend
