"""SF Fonts"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent.name
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = []
build_requirements = []
repo_url = "https://github.com/blaisck/sfwin.git"
repo_name = Path(repo_url).stem


def config():
    configs = []
    # Fonts
    configs.append(
        {"key": "fixed", "value": "'SF Mono,10,-1,5,50,0,0,0,0,0'", "group": "General",}
    )
    configs.append(
        {
            "key": "font",
            "value": "'SF Pro Text,10,-1,5,50,0,0,0,0,0'",
            "group": "General",
        }
    )
    configs.append(
        {
            "key": "menuFont",
            "value": "'SF Pro Text,10,-1,5,50,0,0,0,0,0'",
            "group": "General",
        }
    )

    configs.append(
        {
            "key": "smallestReadableFont",
            "value": "'SF Pro Text,8,-1,5,50,0,0,0,0,0'",
            "group": "General",
        }
    )

    configs.append(
        {
            "key": "toolBarFont",
            "value": "'SF Pro Text,10,-1,5,50,0,0,0,0,0'",
            "group": "General",
        }
    )

    configs.append(
        {
            "key": "activeFont",
            "value": "'SF Pro Text,10,-1,5,50,0,0,0,0,0'",
            "group": "WM",
        }
    )

    u.kwriteconfigs("~/.config/kdeglobals", configs)

    # ========== END KDEGLOBALS ==========


def install(*args, **kwargs):
    u.git_clone(repo_url, G["SOURCES_DIR"])
    # run install.sh
    u.bash_action(action="install", file=__file__, name=component_name)
    config()


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)
