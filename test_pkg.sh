#!/bin/bash
set -e && source pyrel.sh

# build package, install it into virtual
# environment with pip
pyrel_test_begin

# we need this file to run the test
touch __init__.py

# check, that we can import this module by name
# (so it's installed)
python3 -c "import neatest; neatest.run()"

# remove generated package
pyrel_test_end