"""Chili Login Screen"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent.name
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = []
repo_url = "https://github.com/Jonchun/hello.git"
repo_name = Path(repo_url).stem


def install(*args, **kwargs):
    u.git_clone("https://github.com/MarianArlt/kde-plasma-chili.git", G["SOURCES_DIR"])
    # run install.sh
    u.bash_action(action="install", file=__file__, name=component_name)


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)
