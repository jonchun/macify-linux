eval "$(python3 globals.py)"

LATTE_CONF_DIR=~/.config/latte/

# copy layout.latte file as a template
cp -f "$COMPONENTS_DIR/latte_dock/macifyLinux.layout.latte" ${LATTE_CONF_DIR}
chmod 644 ${LATTE_CONF_DIR}/macifyLinux.layout.latte
