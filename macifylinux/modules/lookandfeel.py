"""Look and Feel Module"""
import logging
from pathlib import Path
import tempfile

from macifylinux.components import custom_wallpaper
from macifylinux.components import kde_hello
from macifylinux.components import kde_plasma_chili
from macifylinux.components import mcmojave_cursors
from macifylinux.components import mcmojave_kde
from macifylinux.components import notification_center
from macifylinux.components import os_catalina_icons
from macifylinux.components import sf_fonts

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

logger = logging.getLogger("macifylinux.modules.lookandfeel")

components = [
    custom_wallpaper,
    mcmojave_cursors,
    notification_center,
    os_catalina_icons,
    sf_fonts,
    kde_plasma_chili,
    kde_hello,
]


def install(*args, **kwargs):
    # install mcmojave_kde first as it is the base theme. everything else overwrites it.
    mcmojave_kde.install(*args, **kwargs)
    style = kwargs.get("style", "light")
    if style == "light":
        theme = "McMojave-light"
    elif style == "dark":
        # todo. not tested/working.
        theme = "McMojave"

    # https://userbase.kde.org/KDE_Connect/Tutorials/Useful_commands#Change_look_and_feel
    cmd = "lookandfeeltool -a 'com.github.vinceliuice.{}'".format(theme)
    u.run_shell(cmd, stderr_level=logging.DEBUG)

    for component in components:
        component.install(*args, **kwargs)

    configure(*args, **kwargs)


def upgrade(*args, **kwargs):
    for component in components:
        component.upgrade(*args, **kwargs)


def remove(*args, **kwargs):
    for component in components:
        component.remove(*args, **kwargs)


def configure(*args, **kwargs):
    # ========== START KDEGLOBALS ==========
    configs = []

    # widget style
    configs.append(
        {"group": "General", "key": "widgetStyle", "value": "Breeze",}
    )
    configs.append(
        {"group": "KDE", "key": "widgetStyle", "value": "Breeze",}
    )

    # Dolphin
    u.kwriteconfig(
        {
            "file": "~/.config/dolphinrc",
            "group": "General",
            "key": "ShowFullPath",
            "value": "true",
        }
    )

    # This is to change browsing dolphing to doubleclick rather than single. For some reason it's in globals and not dolphinrc.
    u.kwriteconfig(
        {
            "file": "~/.config/kdeglobals",
            "group": "KDE",
            "key": "SingleClick",
            "value": "false",
        }
    )

    # xsettingsd
    # not sure what this is, but seems important... someone please PR with a better explanation.
    xsettingsd_dir = Path("~/.config/xsettingsd").expanduser()
    xsettingsd_dir.mkdir(parents=True, exist_ok=True)
    xsettingsd_conf = xsettingsd_dir / Path("xsettingsd.conf")
    xsettingsd_template = u.get_template("xsettingsd/xsettingsd.conf")

    if xsettingsd_conf.is_file():
        xsettingsd_conf.rename(
            xsettingsd_conf.with_name("{}.bak".format(xsettingsd_conf.name))
        )
    with xsettingsd_template.open() as f:
        content = f.read()
    # this should later be moved into a search/replace within the icons and cursors components respectively
    content = content.replace("$ICON_THEME", "Os-Catalina-icons").replace(
        "$CURSOR_THEME", "McMojave-cursors"
    )

    with xsettingsd_conf.open("w") as f:
        f.write(content)
    xsettingsd_conf.chmod(0o664)

    # ========== START KWINRC ==========
    # Windows / Window Decorations
    configs = []

    configs.append(
        {"group": "org.kde.kdecoration2", "key": "BorderSize", "value": "None",}
    )

    configs.append(
        {"group": "org.kde.kdecoration2", "key": "BorderSizeAuto", "value": "false",}
    )

    # This section moves the window buttons to the left. Some users might prefer it on the right so will have to add options later.
    configs.append(
        {"group": "org.kde.kdecoration2", "key": "ButtonsOnLeft", "value": "XIA",}
    )
    configs.append(
        {"group": "org.kde.kdecoration2", "key": "ButtonsOnRight", "value": "''",}
    )

    u.kwriteconfigs("~/.config/kwinrc", configs)

    # ========== END KWINRC ==========

    # Change splash screen back to breeze
    u.kwriteconfig(
        {
            "key": "Theme",
            "value": "org.kde.breeze.desktop",
            "group": "KSplash",
            "file": "~/.config/ksplashrc",
        }
    )

    u.restart_kwin()
    u.restart_plasma()
