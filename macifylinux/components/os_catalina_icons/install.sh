#!/bin/bash
eval "$(python3 globals.py)"

REPO_NAME="Os-Catalina-icons"
REPO_URL="https://github.com/zayronxio/Os-Catalina-icons"

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

cp -rf ${SOURCES_DIR}/${REPO_NAME} ${ICONS_DIR}
