"""Bundled Plasmoids"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

logger = logging.getLogger("macifylinux.modules.plasmoids")


def pre(*args, **kwargs):
    pre_applet_window_appmenu()
    u.git_clone(
        "https://github.com/psifidotos/applet-window-title.git", G["SOURCES_DIR"]
    )
    u.git_clone(
        "https://github.com/psifidotos/applet-latte-spacer.git", G["SOURCES_DIR"]
    )
    u.git_clone(
        "https://github.com/psifidotos/applet-latte-separator.git", G["SOURCES_DIR"]
    )
    u.git_clone(
        "https://github.com/MarianArlt/kde-plasmoid-chiliclock.git", G["SOURCES_DIR"]
    )
    u.git_clone("https://github.com/Polunom/mac-inline-battery.git", G["SOURCES_DIR"])
    u.git_clone(
        "https://github.com/psifidotos/applet-latte-sidebar-button.git",
        G["SOURCES_DIR"],
    )
    u.git_clone(
        "https://github.com/Zren/plasma-applet-eventcalendar.git", G["SOURCES_DIR"]
    )
    u.git_clone("https://gitlab.com/divinae/uswitch.git", G["SOURCES_DIR"])
    return True


def run(*args, **kwargs):
    applet_latte_separator = Path("~/sources/applet-latte-separator").expanduser()
    u.install_plasmoid(applet_latte_separator)

    applet_latte_sidebar_button = Path(
        "~/sources/applet-latte-sidebar-button"
    ).expanduser()
    u.install_plasmoid(applet_latte_sidebar_button)

    applet_latte_spacer = Path("~/sources/applet-latte-spacer").expanduser()
    u.install_plasmoid(applet_latte_spacer)

    run_applet_window_appmenu()

    applet_window_title = Path("~/sources/applet-window-title").expanduser()
    u.install_plasmoid(applet_window_title)

    kde_plasmoid_chiliclock = Path(
        "~/sources/kde-plasmoid-chiliclock/org.kde.plasma.chiliclock"
    ).expanduser()
    u.install_plasmoid(kde_plasmoid_chiliclock)

    mac_inline_battery = Path("~/sources/mac-inline-battery").expanduser()
    u.install_plasmoid(mac_inline_battery)

    plasma_applet_eventcalendar = Path(
        "~/sources/plasma-applet-eventcalendar/package/"
    ).expanduser()
    u.install_plasmoid(plasma_applet_eventcalendar, pretty_name="eventcalendar")

    uswitch = Path("~/sources/uswitch/package").expanduser()
    u.install_plasmoid(uswitch, pretty_name="uswitch")


def pre_applet_window_appmenu():
    prerequisites = [
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
    prerequisites_kubuntu_20 = ["libx11-xcb-dev", "libxcb-randr0-dev"]
    prerequisites.extend(prerequisites_kubuntu_20)

    u.apt_install(
        prerequisites, "Window AppMenu plasmoid prerequisites",
    )
    u.git_clone(
        "https://github.com/psifidotos/applet-window-appmenu.git", G["SOURCES_DIR"]
    )


def run_applet_window_appmenu():
    # Need to custom-build. Using this plasmoid because the Global Menu one breaks on multi-monitor setups.
    logger.info(
        "Building Window AppMenu plasmoid (Global Menu). This can take a while..."
    )
    u.run_shell(
        "cd ~/sources/applet-window-appmenu/ && bash ./install.sh",
        stderr_level=logging.DEBUG,
    )
