"""Latte Separator Plasmoid"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = []
repo_url = "https://github.com/psifidotos/applet-latte-separator.git"
repo_name = Path(repo_url).stem


def install(*args, **kwargs):
    u.git_clone(repo_url, G["SOURCES_DIR"])
    u.plasmoid_install(G["SOURCES_DIR"] / Path(repo_name))


def upgrade(*args, **kwargs):
    u.plasmoid_upgrade(G["SOURCES_DIR"] / Path(repo_name))


def remove(*args, **kwargs):
    # run remove.sh
    u.plasmoid_remove(G["SOURCES_DIR"] / Path(repo_name))
