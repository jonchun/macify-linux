"""Kinto - keyboard rebind/mapper to get cmd key shortcuts in Linux"""
import logging
import subprocess

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

logger = logging.getLogger("macifylinux.modules.kinto")


def pre(*args, **kwargs):
    prerequisites = ["xbindkeys", "xdotool", "ibus"]

    u.apt_install(
        prerequisites, "kinto prerequisites",
    )

    """
    logger.info(
        "You may be asked to start the IBus Daemon. Please answer yes. Then, close the preferences window that pops up after."
    )
    """
    u.run_shell("ibus-daemon -drx")
    # u.run_shell("ibus-setup", stderr_level=logging.DEBUG)
    u.run_shell("im-config -n ibus", stderr_level=logging.DEBUG)

    u.git_clone("https://github.com/rbreaves/kinto.git", G["SOURCES_DIR"])
    return True


def run(*args, **kwargs):
    commands = [
        "cd ~/sources/kinto",
        "python3 setup.py",
    ]
    try:
        subprocess.run(" && ".join(commands), shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Problem while installing kinto: %s", e)
        logger.debug("", exc_info=True)
