"""Albert"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = [
    "cmake",
    "libmuparser-dev",
    "libqt5charts5-dev",
    "libqt5svg5-dev",
    "libqt5x11extras5-dev",
    "python3-dev",
    "python3-distutils",
    "qtdeclarative5-dev",
]
repo_url = "https://github.com/Jonchun/albert.git"
repo_name = Path(repo_url).stem


def install(*args, **kwargs):
    u.git_clone(repo_url, G["SOURCES_DIR"])
    # run install.sh
    u.bash_action(action="install", file=__file__, name=component_name)

    # run configure.sh
    u.bash_action(action="configure", file=__file__, name=component_name)

    # start albert
    albert_desktop_file = Path("/usr/local/share/applications/albert.desktop")
    u.run_shell_bg("nohup /bin/sh {}".format(albert_desktop_file.resolve()))


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)
