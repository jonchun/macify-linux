"""Albert"""
import logging
from pathlib import Path
import time

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent.name
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = [
    "build-essential",
    "cmake",
    "extra-cmake-modules",
    "gettext",
    "git",
    "libkf5activities-dev",
    "libkf5archive-dev",
    "libkf5crash-dev",
    "libkf5declarative-dev",
    "libkf5iconthemes-dev",
    "libkf5newstuff-dev",
    "libkf5notifications-dev",
    "libkf5plasma-dev",
    "libkf5wayland-dev",
    "libkf5windowsystem-dev",
    "libkf5xmlgui-dev",
    "libqt5x11extras5-dev",
    "libsm-dev",
    "libxcb-util-dev",
    "libxcb-util0-dev",
    "qtdeclarative5-dev",
]

# needed to add these packages when attempting to compile in Kubuntu 18.04
apt_requirements_kubuntu_18 = ["libkf5sysguard-dev"]
apt_requirements.extend(apt_requirements_kubuntu_18)

repo_url = "https://github.com/KDE/latte-dock.git"
repo_name = Path(repo_url).stem


def install(*args, **kwargs):
    u.git_clone(repo_url, G["SOURCES_DIR"])
    # run install.sh
    u.bash_action(action="install", file=__file__, name=component_name, stderr_level=logging.DEBUG)

    # Start and stop latte once after installing in order to generate the default configs.
    start_latte()
    time.sleep(2)
    stop_latte()

    # run configure.sh
    u.bash_action(action="configure", file=__file__, name=component_name)

    # remove any default panels we find automatically
    script = u.get_template("removeDefaultPanels.js")
    u.eval_plasma_script(script)

    # Edit latte config files
    u.kwriteconfig(
        {
            "file": "~/.config/lattedockrc",
            "group": "UniversalSettings",
            "key": "currentLayout",
            "value": "macifyLinux",
        }
    )
    u.kwriteconfig(
        {
            "file": "~/.config/lattedockrc",
            "group": "UniversalSettings",
            "key": "lastNonAssignedLayout",
            "value": "macifyLinux",
        }
    )
    start_latte()


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)


def start_latte():
    logger.debug("Starting Latte Dock.")
    u.run_shell_bg("gtk-launch org.kde.latte-dock.desktop")


def stop_latte():
    logger.debug("Stopping Latte Dock.")
    u.run_shell_bg("killall -9 latte-dock")
