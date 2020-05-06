"""MacifyLinux LookAndFeel Package"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent.name
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = []
build_requirements = []
light_laf = u.get_template("lookandfeel/com.github.jonchun.macify-linux-light")
dark_laf = u.get_template("lookandfeel/com.github.jonchun.macify-linux-dark")


def install(*args, **kwargs):
    u.plasmoid_tool(
        light_laf,
        action="install",
        package_type="Plasma/LookAndFeel",
        pretty_name="macify-linux-light lookandfeel",
    )
    u.plasmoid_tool(
        dark_laf,
        action="install",
        package_type="Plasma/LookAndFeel",
        pretty_name="macify-linux-dark lookandfeel",
    )


def upgrade(*args, **kwargs):
    u.plasmoid_tool(
        light_laf,
        action="upgrade",
        package_type="Plasma/LookAndFeel",
        pretty_name="macify-linux-light lookandfeel",
    )
    u.plasmoid_tool(
        dark_laf,
        action="upgrade",
        package_type="Plasma/LookAndFeel",
        pretty_name="macify-linux-dark lookandfeel",
    )


def remove(*args, **kwargs):
    u.plasmoid_tool(
        light_laf,
        action="remove",
        package_type="Plasma/LookAndFeel",
        pretty_name="macify-linux-light lookandfeel",
    )
    u.plasmoid_tool(
        dark_laf,
        action="remove",
        package_type="Plasma/LookAndFeel",
        pretty_name="macify-linux-dark lookandfeel",
    )
