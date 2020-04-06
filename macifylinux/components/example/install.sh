#!/bin/bash
# u.run_shell will automatically cd the current shell to the currect python module directory (where utils.py and globals.py reside)
eval "$(python3 globals.py)"
# The ifmain() part of globals.py returns a string that sets a bunch of bash variables. This allows you to use the global variabls defined in python
# as part of bash.
# e.g. echo $SOURCES_DIR should give you the full path to "~/sources/" 
REPO_NAME="example"
REPO_URL="https://github.com/examplerepo"

if [ ! -d ${SOURCES_DIR}/${REPO_NAME} ]
then
    # what to do if directory doesn't exist
    cd ${SOURCES_DIR}
    git clone $REPO_URL $REPO_NAME
else
    # what to do if directory already exists
    cd ${SOURCES_DIR}/${REPO_NAME}
    git fetch
fi

### do some install stuff.
# "$SOURCES_DIR/$REPO_NAME"
# ./configure
# make
# sudo make install
