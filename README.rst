Guess Who?
==========
:Info: A Django implementation of the 1979 game [Guess
       Who](http://en.wikipedia.org/wiki/Guess_Who%3F)
:Authors: Steven Challis (http://schallis.com)
:Requires: Python 2.7 (see requirements.txt)

Running tests
=============
The entire test suite can be run by executing the `ci-build.sh` script. This
will also generate linting (`pep8.txt`, `pylint.txt`) and coverage reports
(`htmlcov/index.html`).


TODO:
=====
* Enforce asking questions in turns
* Game creation
* Game joining
* Prevent more than two players being added to a game
* Move view logic to API endpoints and implement Ajax frontend
