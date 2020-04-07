#!/bin/bash
eval "$(python3 globals.py)"

cp -rf ${SOURCES_DIR}/sfwin/SFCompact ${FONTS_DIR}
cp -rf ${SOURCES_DIR}/sfwin/SFMono ${FONTS_DIR}
cp -rf ${SOURCES_DIR}/sfwin/SFPro ${FONTS_DIR}

# Refresh font cache
fc-cache -fv
