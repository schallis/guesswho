#!/bin/sh

set -e

fail () {
    MESSAGE=$1
    echo "FAILURE: $MESSAGE"
    exit 1
}

log () {
    echo -n "[$(date)] "
    echo $1
}

start () {
    log "Starting: $1"
    START=$(date +%s.%N)
}

end () {
    END=$(date +%s.%N)
    DIFF=$(echo "$END - $START" | bc)
    log "Finished: $1 (took $DIFF seconds)"
    START=
}

do_build () {
    PROJECT=$1

    #remove .pyc files
    start "REMOVING .pyc FILES"
    find ./${PROJECT} -name "*.pyc" -exec rm {} \;
    end "REMOVING .pyc FILES"

    # Sync db (required for tests)
    PYTHONPATH=. DJANGO_SETTINGS_MODULE="${PROJECT}.settings.test_settings" \
        django-admin.py syncdb --noinput

    # Run tests with coverage
    start "RUNNING TESTS"
    coverage erase
    PYTHONPATH=. DJANGO_SETTINGS_MODULE="${PROJECT}.settings.test_settings" \
        coverage run ${PROJECT}/manage.py test ${PROJECT} \
        --noinput -v2 \
        || fail "Tests failed"
    end "RUNNING TESTS"

    start "GENERATING COVERAGE REPORTS"
    coverage xml
    coverage html -d htmlcov
    end "GENERATING COVERAGE REPORTS"

    # PEP8
    start "RUNNING pep8"
    pep8 -r ${PROJECT} > pep8.txt || echo "PEP-8 violations"
    end "RUNNING pep8"

    # Pylint
    start "RUNNING pylint"
    pylint --rcfile=.pylintrc ${PROJECT} > pylint.txt \
        || echo "Pylint violations"
    end "RUNNING pylint"
}

do_build guesswho
