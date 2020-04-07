eval "$(python3 globals.py)"

# Start the ibus-daemon and run im-config before starting kinto. I don't actually know what this does.
ibus-daemon -drx
im-config -n ibus

cd ${SOURCES_DIR}/kinto
python3 setup.py

# Restart the keyswap service for good measure. I've had it get stuck sometimes.
systemctl --user restart keyswap
