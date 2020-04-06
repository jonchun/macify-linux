"""Plasmoids needed"""
from macifylinux.components import applet_latte_separator
from macifylinux.components import applet_latte_sidebar_button
from macifylinux.components import applet_latte_spacer
from macifylinux.components import applet_window_title
from macifylinux.components import kde_plasmoid_chiliclock
from macifylinux.components import mac_inline_battery
from macifylinux.components import uswitch

components = [
    applet_latte_separator,
    applet_latte_sidebar_button,
    applet_latte_spacer,
    applet_window_title,
    kde_plasmoid_chiliclock,
    mac_inline_battery,
    uswitch,
]


def install(*args, **kwargs):
    for component in components:
        component.install(*args, **kwargs)


def upgrade(*args, **kwargs):
    for component in components:
        component.upgrade(*args, **kwargs)


def remove(*args, **kwargs):
    for component in components:
        component.remove(*args, **kwargs)
