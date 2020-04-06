#!/bin/bash
eval "$(python3 globals.py)"
cd "$SOURCES_DIR/$REPO_NAME"
bash ./uninstall.sh
