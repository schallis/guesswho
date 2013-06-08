#!/bin/bash
set -e

check_requirements () {
   # Verify whether any requirement file has changed.
   # Avoid the creation of a virtual environment if nothing has changed.

   VIRTUALENVS_DIR=$HOME/virtualenvs

   unamestr=`uname`
   if [[ "$unamestr" == 'Darwin' ]]; then
       HASH=$(tar c requirements/ | md5)
   else
       HASH=$(tar c requirements/ | md5sum)
   fi

   if [[ -d ${VIRTUALENVS_DIR}/${HASH} ]]; then
      echo "Reusing virtual environment ${VIRTUALENVS_DIR}/${HASH}"
      . ${VIRTUALENVS_DIR}/${HASH}/bin/activate
   else
      echo "Requirements files changed, creating a new virtual environment."
      create_virtualenv ${VIRTUALENVS_DIR}/${HASH}
   fi
}


create_virtualenv () {
   # Create a clean virtual environment
   # Parameters: virtualenv's path

   VIRTUALENV=$1
   rm -rf $VIRTUALENV
   virtualenv --no-site-packages -p python2.7 $VIRTUALENV \
       || { echo "virtualenv failed"; exit -1; }

   . $VIRTUALENV/bin/activate
   pip install -i http://c.pypi.python.org/simple -U setuptools
   pip install -i http://c.pypi.python.org/simple -U pip

   # Reset the path so that pip is picked up from the right location
   # (avoid conflict with a system-wide installation of pip)
   . $VIRTUALENV/bin/activate

   pip install -i http://c.pypi.python.org/simple \
       -r requirements/test.txt \
       || { echo "pip failed"; exit -1; }
}
