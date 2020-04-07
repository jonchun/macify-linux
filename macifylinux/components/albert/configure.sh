eval "$(python3 globals.py)"

ALBERT_CONF_DIR=~/.config/albert/
mkdir -p ${ALBERT_CONF_DIR}

# copy conf file as a template
cp "$COMPONENTS_DIR/albert/albert.conf" ${ALBERT_CONF_DIR}
chmod 664 ${ALBERT_CONF_DIR}/albert.conf

# This prevents the albert configuration menu from popping up on first start. Might need to update this later.
echo "0.16.1" > ${ALBERT_CONF_DIR}/last_used_version
chmod 664 ${ALBERT_CONF_DIR}/last_used_version

# Configure autostart
mkdir -p ~/.config/autostart
rm -f ~/.config/autostart/albert.desktop
ln -s /usr/local/share/applications/albert.desktop ~/.config/autostart/
