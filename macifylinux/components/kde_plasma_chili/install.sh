#!/bin/bash
eval "$(python3 globals.py)"

REPO_NAME="kde-plasma-chili"
REPO_URL="https://github.com/MarianArlt/kde-plasma-chili.git"

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

sudo cp -Trf ${SOURCES_DIR}/${REPO_NAME} ${SDDM_THEMES_DIR}/plasma-chili
