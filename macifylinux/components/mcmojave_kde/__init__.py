"""Albert"""
import logging
from pathlib import Path

import macifylinux.utils as u

apt_requirements = []
component_name = "mcmojave_kde"
logger = logging.getLogger("macifylinux.components.{}".format(component_name))


def install(*args, **kwargs):
    # run install.sh
    u.bash_action(action="install", file=__file__, name=component_name)


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)
