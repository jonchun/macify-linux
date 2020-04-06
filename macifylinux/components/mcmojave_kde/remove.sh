#!/bin/bash
eval "$(python3 globals.py)"

cd ${SOURCES_DIR}/McMojave-kde
bash ./uninstall.sh
