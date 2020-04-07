"""Hello Window Decorations"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent.name
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = [
    "build-essential",
    "cmake",
    "extra-cmake-modules",
    "g++",
    "gettext",
    "kinit-dev",
    "kwin-dev",
    "libkdecorations2-dev",
    "libkf5config-dev",
    "libkf5configwidgets-dev",
    "libkf5coreaddons-dev",
    "libkf5crash-dev",
    "libkf5globalaccel-dev",
    "libkf5guiaddons-dev",
    "libkf5kio-dev",
    "libkf5notifications-dev",
    "libkf5package-dev",
    "libkf5windowsystem-dev",
    "libqt5x11extras5-dev",
    "qtbase5-dev",
    "qtdeclarative5-dev",
    "qttools5-dev",
]
repo_url = "https://github.com/Jonchun/hello.git"
repo_name = Path(repo_url).stem


def install(*args, **kwargs):
    u.git_clone(repo_url, G["SOURCES_DIR"])
    # run install.sh
    u.bash_action(action="install", file=__file__, name=component_name, stderr_level=logging.DEBUG)


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)
