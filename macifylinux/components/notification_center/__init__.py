"""Mac Inline Battery Plasmoid"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent.name
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = []


def install(*args, **kwargs):
    # currently, notification center just consists of tweaking a few default values for the built in notifications plasmoid.
    # will hopefully change this soon to be better with a custom plasmoid
    # ========== START PLASMANOTIFYRC ==========
    configs = []

    configs.append(
        {"group": "Notifications", "key": "LowPriorityHistory", "value": "true",}
    )

    configs.append(
        {"group": "Notifications", "key": "PopupPosition", "value": "TopRight",}
    )

    configs.append(
        {"group": "Notifications", "key": "PopupTimeout", "value": "5000",}
    )

    u.kwriteconfigs("~/.config/plasmanotifyrc", configs)

    # ========== END PLASMANOTIFYRC ==========


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # Not sure how to unconfigure these to default. Should look into the kwriteconfig5 options
    pass
