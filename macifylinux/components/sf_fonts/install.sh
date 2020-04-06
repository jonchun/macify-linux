#!/bin/bash
eval "$(python3 globals.py)"

REPO_NAME="sfwin"
REPO_URL="https://github.com/blaisck/sfwin.git"

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

# -T, --no-target-directory treat DEST as a normal file
cp -Tr "$SOURCES_DIR/$REPO_NAME/SFCompact" "$FONTS_DIR/SFCompact"
cp -Tr "$SOURCES_DIR/$REPO_NAME/SFMono" "$FONTS_DIR/SFMono"
cp -Tr "$SOURCES_DIR/$REPO_NAME/SFPro" "$FONTS_DIR/SFPro"

# Clear font cache
fc-cache -fv