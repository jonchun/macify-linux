"""Chili Login Screen"""
import logging
from pathlib import Path
import tempfile

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent.name
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = []
build_requirements = []
repo_url = "https://github.com/Jonchun/hello.git"
repo_name = Path(repo_url).stem


def configure():
    # ========== START SDDM ==========
    # On KDE Neon, the file is at /etc/sddm.conf.d/kde_settings.conf
    # this might be different in other distros.
    u.kwriteconfig(
        {
            "key": "Current",
            "value": "plasma-chili",
            "group": "Theme",
            "file": "/etc/sddm.conf.d/kde_settings.conf",
        },
        root=True,
    )

    # Configure wallpaper of SDDM
    with u.get_template("sddm/theme.conf.user").open() as f:
        sddm_theme_conf = f.read()
    sddm_theme_conf = sddm_theme_conf.replace(
        "$BACKGROUND_IMAGE", G["DEFAULT_WALLPAPER"]
    )

    default_wallpaper = G["WALLPAPERS_DIR"] / G["DEFAULT_WALLPAPER"]

    # Create theme.user.conf (points to wallpaper) and move it to theme directory. Doing it weird like this because sudo is required.
    tmp_file = tempfile.NamedTemporaryFile("w", delete=False)
    tmp_file.write(sddm_theme_conf)
    tmp_file.close()
    logger.debug("Wallpaper: %s", default_wallpaper)
    u.cp(default_wallpaper, "/usr/share/sddm/themes/plasma-chili", root=True)
    tmp_file_path = Path(tmp_file.name)
    tmp_file_path.chmod(0o664)
    u.cp(
        tmp_file_path, "/usr/share/sddm/themes/plasma-chili/theme.conf.user", root=True
    )
    tmp_file_path.unlink()

    # ========== END SDDM ==========


def install(*args, **kwargs):
    u.git_clone("https://github.com/MarianArlt/kde-plasma-chili.git", G["SOURCES_DIR"])
    # run install.sh
    u.bash_action(action="install", file=__file__, name=component_name)
    configure()

    # ========== END SDDM ==========


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)
