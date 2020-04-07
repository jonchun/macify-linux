#!/bin/bash
eval "$(python3 globals.py)"

sudo cp -Trf ${SOURCES_DIR}/kde-plasma-chili ${SDDM_THEMES_DIR}/plasma-chili
