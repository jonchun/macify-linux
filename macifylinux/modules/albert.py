"""Albert - A Spotlight search replacement"""
import logging
from pathlib import Path
import subprocess

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

logger = logging.getLogger("macifylinux.modules.albert")


def pre(*args, **kwargs):
    prerequisites = [
        "cmake",
        "libqt5x11extras5-dev",
        "libqt5svg5-dev",
        "qtdeclarative5-dev",
        "python3-distutils",
        "libqt5charts5-dev",
        "libmuparser-dev",
        "python3-dev",
        "python3-distutils",
    ]
    u.apt_install(
        prerequisites, "albert prerequisites",
    )
    u.git_clone(
        "https://github.com/Jonchun/albert.git",
        G["SOURCES_DIR"],
        flags="--branch MacifyLinux --recursive",
    )
    return True


def run(*args, **kwargs):
    # Need to custom-build albert due to a bug with icons
    # https://github.com/albertlauncher/albert/issues/778

    albert_build = G["SOURCES_DIR"] / Path("albert-build")
    albert_build.mkdir(parents=True, exist_ok=True)
    logger.info("Building albert. This can take a while...")
    commands = [
        "cd ~/sources/albert-build/",
        "cmake ../albert -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Debug",
        "make",
        "sudo make install",
    ]
    u.run_shell(
        " && ".join(commands), stderr_level=logging.DEBUG,
    )

    # autostart albert
    albert_desktop_file = Path("/usr/local/share/applications/albert.desktop")
    autostart_dir = Path("~/.config/autostart").expanduser()
    autostart_dir.mkdir(parents=True, exist_ok=True)

    u.setup_symlink(albert_desktop_file, autostart_dir, target_is_directory=True)

    # albert configuration
    albert_conf = u.get_template("albert/albert.conf")
    albert_conf_dir = Path("~/.config/albert").expanduser()
    albert_conf_dir.mkdir(parents=True, exist_ok=True)
    u.copy_file(albert_conf, albert_conf_dir / albert_conf.name)

    last_used_version = albert_conf_dir / Path("last_used_version")
    with last_used_version.open("w") as f:
        f.write("0.16.1")

    # start albert
    # execute it directly via Popen so that there are no open pipes when program exits.
    subprocess.Popen(
        "nohup /bin/sh {} > /dev/null 2>&1 &".format(albert_desktop_file.resolve()),
        shell=True,
    )
    return True
