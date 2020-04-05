"""This module is responsible for all of the theming/fonts/icons"""
import logging
from pathlib import Path
import tempfile

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

logger = logging.getLogger("macifylinux.modules.lookandfeel.configure")


def configure(*args, **kwargs):
    options = kwargs.get("options", {})
    style = options.get("style", "light")

    # https://userbase.kde.org/KDE_Connect/Tutorials/Useful_commands#Change_look_and_feel
    if style == "light":
        theme = "McMojave-light"
        plasma_theme = "hellolight"
        color_scheme = "HelloLight"
        #color_scheme = "McMojaveLight"
    elif style == "dark":
        # todo. not tested/working.
        theme = "McMojave"
        plasma_theme = "hellodark"
        color_scheme = "HelloDark"
        #color_scheme = "McMojave"

    # run the lookandfeeltool
    cmd = "lookandfeeltool -a 'com.github.vinceliuice.{}'".format(theme)
    u.run_shell(cmd, stderr_level=logging.DEBUG)

    u.stop_plasma()

    # ========== START KDEGLOBALS ==========
    configs = []

    # widget style
    configs.append(
        {"key": "widgetStyle", "value": "Breeze", "group": "General",}
    )
    configs.append(
        {"key": "widgetStyle", "value": "Breeze", "group": "KDE",}
    )

    # colors
    configs.append(
        {"key": "Name", "value": color_scheme, "group": "General",}
    )
    configs.append(
        {"key": "ColorScheme", "value": color_scheme, "group": "General",}
    )

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

    # icons
    configs.append(
        {"key": "Theme", "value": "Os-Catalina-icons", "group": "Icons",}
    )

    u.kwriteconfigs("~/.config/kdeglobals", configs)

    # ========== END KDEGLOBALS ==========

    # plasma theme
    # hellolight
    u.kwriteconfig(
        {"key": "name", "value": plasma_theme, "group": "Theme", "file": "~/.config/plasmarc",}
    )

    # Dolphin
    u.kwriteconfig(
        {
            "key": "ShowFullPath",
            "value": "true",
            "group": "General",
            "file": "~/.config/dolphinrc",
        }
    )
    # This is to change browsing dolphing to doubleclick rather than single. For some reason it's in globals and not dolphin.
    u.kwriteconfig(
        {
            "key": "SingleClick",
            "value": "false",
            "group": "KDE",
            "file": "~/.config/kdeglobals",
        }
    )

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

    default_wallpaper = G["WALLPAPER_DIR"] / G["DEFAULT_WALLPAPER"]

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

    # xsettingsd
    # not sure what this is, but seems important...
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
        {"key": "BorderSize", "value": "None", "group": "org.kde.kdecoration2",}
    )

    configs.append(
        {"key": "BorderSizeAuto", "value": "false", "group": "org.kde.kdecoration2",}
    )
    configs.append(
        {"key": "ButtonsOnLeft", "value": "XIA", "group": "org.kde.kdecoration2",}
    )
    configs.append(
        {"key": "ButtonsOnRight", "value": "''", "group": "org.kde.kdecoration2",}
    )
    configs.append(
        {"key": "library", "value": "org.kde.hello", "group": "org.kde.kdecoration2",}
    )
    configs.append(
        {"key": "theme", "value": "hello", "group": "org.kde.kdecoration2",}
    )

    u.kwriteconfigs("~/.config/kwinrc", configs)

    # ========== END KWINRC ==========

    # ========== START PLASMANOTIFYRC ==========
    configs = []

    configs.append(
        {"key": "LowPriorityHistory", "value": "true", "group": "Notifications",}
    )

    configs.append(
        {"key": "PopupPosition", "value": "TopRight", "group": "Notifications",}
    )

    configs.append(
        {"key": "PopupTimeout", "value": "5000", "group": "Notifications",}
    )

    u.kwriteconfigs("~/.config/plasmanotifyrc", configs)

    # ========== END PLASMANOTIFYRC ==========

    # Change splash screen back to breeze
    u.kwriteconfig(
        {
            "key": "Theme",
            "value": "org.kde.breeze.desktop",
            "group": "KSplash",
            "file": "~/.config/ksplashrc",
        }
    )

    # Configure wallpaper of lockscreen
    wallpaper = G["WALLPAPER_DIR"] / Path("kym-ellis-RPT3AjdXlZc-unsplash.jpg")
    u.kwriteconfig(
        {
            "key": "Image",
            "value": "file://{}".format(wallpaper),
            "group": ["Greeter", "Wallpaper", "org.kde.image", "General"],
            "file": "~/.config/kscreenlockerrc",
        }
    )

    u.start_plasma()
    u.restart_kwin()
