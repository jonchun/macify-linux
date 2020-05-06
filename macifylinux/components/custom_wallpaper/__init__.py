"""Custom Wallpaper"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

apt_requirements = ["curl"]
build_requirements = []
component_name = "custom_wallpaper"
logger = logging.getLogger("macifylinux.components.{}".format(component_name))


def install(*args, **kwargs):
    # run install.sh
    u.bash_action(action="install", file=__file__, name=component_name)

    # change desktop wallapaper
    wallpaper = G["WALLPAPERS_DIR"] / Path(G["DEFAULT_WALLPAPER"])
    u.change_desktop_wallpaper(wallpaper)

    # change lockscreen wallpaper
    u.kwriteconfig(
        {
            "key": "Image",
            "value": "file://{}".format(wallpaper),
            "group": ["Greeter", "Wallpaper", "org.kde.image", "General"],
            "file": "~/.config/kscreenlockerrc",
        }
    )


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)
