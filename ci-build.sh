#!/bin/bash

set -e

# Intended to run a full build within a CI environment or a developer's
# workstation.

. ./create-virtualenv.sh

# Check and create the virtualenv if needed
check_requirements

# Perform the build
./build.sh
