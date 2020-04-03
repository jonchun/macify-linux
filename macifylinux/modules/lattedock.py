"""latte-dock - Dock/Panel"""
import logging
import time

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

logger = logging.getLogger("macifylinux.modules.lattedock")


def pre(*args, **kwargs):
    prerequisites = [
        "build-essential",
        "cmake",
        "extra-cmake-modules",
        "gettext",
        "git",
        "libkf5activities-dev",
        "libkf5archive-dev",
        "libkf5crash-dev",
        "libkf5declarative-dev",
        "libkf5iconthemes-dev",
        "libkf5newstuff-dev",
        "libkf5notifications-dev",
        "libkf5plasma-dev",
        "libkf5wayland-dev",
        "libkf5windowsystem-dev",
        "libkf5xmlgui-dev",
        "libqt5x11extras5-dev",
        "libsm-dev",
        "libxcb-util-dev",
        "libxcb-util0-dev",
        "qtdeclarative5-dev",
    ]

    u.apt_install(
        prerequisites, "latte-dock prerequisites",
    )

    u.git_clone("https://github.com/KDE/latte-dock.git", G["SOURCES_DIR"])
    return True


def run(*args, **kwargs):
    # Need to custom-build to get latest latte for sidebar functionality.
    logger.info("Building latte-dock. This can take a while...")
    u.run_shell(
        "cd ~/sources/latte-dock/ && bash ./install.sh", stderr_level=logging.DEBUG,
    )
    # Start latte immediately after building it. This is to generate the initial configs.
    u.start_latte()

    # wait 2 seconds to allow latte to start up
    time.sleep(2)
    configure_latte()


def configure_latte():
    u.stop_latte()
    logger.info("Removing default panels and configuring latte.")
    script = u.get_template("removeDefaultPanels.js")
    u.eval_plasma_script(script)

    latte_template = u.get_template("lattedock/macifyLinux.layout.latte")
    latte_layout_conf = G["LATTE_DIR"] / latte_template.name
    u.copy_file(latte_template, latte_layout_conf)
    latte_layout_conf.chmod(0o664)

    u.kwriteconfig(
        {
            "key": "currentLayout",
            "value": "macifyLinux",
            "group": "UniversalSettings",
            "file": "~/.config/lattedockrc",
        }
    )
    u.kwriteconfig(
        {
            "key": "lastNonAssignedLayout",
            "value": "macifyLinux",
            "group": "UniversalSettings",
            "file": "~/.config/lattedockrc",
        }
    )
    u.start_latte()
