"""Window App Menu"""
import logging
from pathlib import Path
import subprocess

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent.name
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = [
    "cmake",
    "extra-cmake-modules",
    "libkdecorations2-dev",
    "qtdeclarative5-dev",
    "libkf5windowsystem-dev",
    "libkf5plasma-dev",
    "libkf5configwidgets-dev",
    "libsm-dev",
    "libqt5x11extras5-dev",
]
# needed to add these packages when attempting to compile in Kubuntu 20.04
apt_requirements_kubuntu_20 = ["libx11-xcb-dev", "libxcb-randr0-dev"]
apt_requirements.extend(apt_requirements_kubuntu_20)

repo_url = "https://github.com/psifidotos/applet-window-appmenu.git"
repo_name = Path(repo_url).stem


def install(*args, **kwargs):
    u.git_clone(repo_url, G["SOURCES_DIR"])
    # run install.sh
    u.bash_action(
        action="install", file=__file__, name=component_name, stderr_level=logging.DEBUG
    )


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)
