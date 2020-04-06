#!/bin/bash
eval "$(python3 globals.py)"

REPO_NAME="McMojave-kde"
REPO_URL="https://github.com/vinceliuice/McMojave-kde.git"

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

cd "$SOURCES_DIR/$REPO_NAME"
bash ./install.sh
