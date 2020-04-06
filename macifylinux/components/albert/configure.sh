echo "$(pwd)2"
eval "$(python3 globals.py)"

# cp template conf file
cp "$COMPONENTS_DIR/albert/albert.conf" ~/.config/albert/

# This prevents the albert configuration menu from popping up on first start.
echo "0.16.1" > ~/.config/albert/last_used_version

# Configure autostart
mkdir -p ~/.config/autostart
rm -f ~/.config/autostart/albert.desktop
ln -s /usr/local/share/applications/albert.desktop ~/.config/autostart/
