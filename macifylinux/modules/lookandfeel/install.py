"""This module is responsible for all of the theming/fonts/icons"""
import logging
from pathlib import Path
import subprocess

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

logger = logging.getLogger("macifylinux.modules.lookandfeel.configure")


def install(*args, **kwargs):
    install_cursors()
    install_fonts()
    install_icons()
    install_login_screen()
    install_themes()
    install_wallpapers()
    install_window_decorations()


def install_cursors():
    logger.info("Installing cursors.")
    u.git_clone("https://github.com/vinceliuice/McMojave-cursors.git", G["SOURCES_DIR"])
    mcmojave_cursors = Path("~/sources/McMojave-cursors/dist").expanduser()
    """
    u.setup_symlink(mcmojave_cursors, G['ICONS_DIR'] / Path("McMojave-cursors"))
    u.copy_file(
        mcmojave_cursors, G['ICONS_DIR'] / Path("McMojave-cursors"), recursive=True,
    )
    """
    u.cp(mcmojave_cursors, G["ICONS_DIR"] / Path("McMojave-cursors"), "Tr")


def install_fonts():
    logger.info("Installing SF fonts.")
    u.git_clone("https://github.com/blaisck/sfwin.git", G["SOURCES_DIR"])

    installed = 0
    sf_compact = Path("~/sources/sfwin/SFCompact").expanduser()
    installed += int(
        u.setup_symlink(sf_compact, G["FONTS_DIR"], target_is_directory=True)
    )
    sf_mono = Path("~/sources/sfwin/SFMono").expanduser()
    installed += int(u.setup_symlink(sf_mono, G["FONTS_DIR"], target_is_directory=True))
    sf_pro = Path("~/sources/sfwin/SFPro").expanduser()
    installed += int(u.setup_symlink(sf_pro, G["FONTS_DIR"], target_is_directory=True))

    if installed > 0:
        logger.info(
            "Installed %s fonts. Refreshing font cache. This may take a while.",
            installed,
        )
        u.run_shell("fc-cache -fv")
    else:
        logger.warning("No fonts were installed. They probably already existed.")


def install_icons():
    logger.info("Installing icon packs.")

    u.git_clone("https://github.com/vinceliuice/McMojave-circle.git", G["SOURCES_DIR"])
    u.git_clone("https://github.com/zayronxio/Os-Catalina-icons", G["SOURCES_DIR"])

    # This install script does a lot... don't want to figure out/translate it into python right now.
    try:
        u.run_shell(
            "cd ~/sources/McMojave-circle/ && bash ./install.sh",
            stderr_level=logging.DEBUG,
        )
    except subprocess.CalledProcessError:
        logger.error("Unable to install McMojave-circle icon pack!")

    catalina_icons = Path("~/sources/Os-Catalina-icons").expanduser()
    u.cp(catalina_icons, G["ICONS_DIR"], "rf")

    """
    u.copy_file(
        catalina_icons, G['ICONS_DIR'] / catalina_icons.name, recursive=True,
    )
    installed += int(
        u.setup_symlink(catalina_icons, G['ICONS_DIR'], target_is_directory=True)
    )
    """


def install_login_screen():
    logger.info("Installing Login Screen.")

    kde_plasma_chili = u.git_clone(
        "https://github.com/MarianArlt/kde-plasma-chili.git", G["SOURCES_DIR"]
    )
    theme_path = Path("/usr/share/sddm/themes/plasma-chili")
    if theme_path.is_dir():
        u.run_shell("rm -rf {}".format(theme_path), root=True)

    u.cp(kde_plasma_chili, theme_path, flags="r", root=True)


def install_themes():
    logger.info("Installing KDE themes.")

    u.git_clone("https://github.com/vinceliuice/McMojave-kde.git", G["SOURCES_DIR"])

    mcmojave_kde = Path("~/sources/McMojave-kde").expanduser()

    u.setup_symlink(
        mcmojave_kde / Path("aurorae/McMojave"),
        G["AURORAE_DIR"],
        target_is_directory=True,
    )
    u.setup_symlink(
        mcmojave_kde / Path("aurorae/McMojave-light"),
        G["AURORAE_DIR"],
        target_is_directory=True,
    )

    u.setup_symlink(
        mcmojave_kde / Path("Kvantum/McMojave"),
        G["KVANTUM_DIR"],
        target_is_directory=True,
    )
    u.setup_symlink(
        mcmojave_kde / Path("Kvantum/McMojave-light"),
        G["KVANTUM_DIR"],
        target_is_directory=True,
    )

    u.setup_symlink(
        mcmojave_kde / Path("plasma/desktoptheme/McMojave"),
        G["PLASMA_DIR"],
        target_is_directory=True,
    )
    u.setup_symlink(
        mcmojave_kde / Path("plasma/desktoptheme/McMojave-light"),
        G["PLASMA_DIR"],
        target_is_directory=True,
    )
    u.setup_symlink(
        mcmojave_kde / Path("color-schemes/McMojave.colors"),
        G["PLASMA_DIR"] / Path("McMojave/colors"),
    )
    u.setup_symlink(
        mcmojave_kde / Path("color-schemes/McMojaveLight.colors"),
        G["PLASMA_DIR"] / Path("McMojave-light/colors"),
    )

    u.setup_symlink(
        mcmojave_kde / Path("color-schemes/McMojave.colors"),
        G["COLOR_SCHEMES_DIR"],
        target_is_directory=True,
    )
    u.setup_symlink(
        mcmojave_kde / Path("color-schemes/McMojaveLight.colors"),
        G["COLOR_SCHEMES_DIR"],
        target_is_directory=True,
    )

    u.setup_symlink(
        mcmojave_kde / Path("plasma/look-and-feel/com.github.vinceliuice.McMojave"),
        G["LOOK_FEEL_DIR"],
        target_is_directory=True,
    )
    u.setup_symlink(
        mcmojave_kde
        / Path("plasma/look-and-feel/com.github.vinceliuice.McMojave-light"),
        G["LOOK_FEEL_DIR"],
        target_is_directory=True,
    )

    panel_layout = mcmojave_kde / Path(
        "plasma/layout-templates/org.github.desktop.McMojavePanel"
    )
    u.copy_file(
        panel_layout, G["LAYOUT_DIR"] / panel_layout.name, recursive=True,
    )


def install_wallpapers():
    wallpaper = G["WALLPAPER_DIR"] / Path(G["DEFAULT_WALLPAPER"])
    u.download_url(
        "https://unsplash.com/photos/RPT3AjdXlZc/download?force=true", wallpaper
    )
    u.change_wallpaper(wallpaper)


def install_window_decorations():
    # u.apt_add_ppa("krisives/kde-hello")
    # u.apt_install(["kde-hello"], "kde-hello window decorations")

    prerequisites = [
        "build-essential",
        "cmake",
        "extra-cmake-modules",
        "g++",
        "gettext",
        "kinit-dev",
        "kwin-dev",
        "libkdecorations2-dev",
        "libkf5config-dev",
        "libkf5configwidgets-dev",
        "libkf5coreaddons-dev",
        "libkf5crash-dev",
        "libkf5globalaccel-dev",
        "libkf5guiaddons-dev",
        "libkf5kio-dev",
        "libkf5notifications-dev",
        "libkf5package-dev",
        "libkf5windowsystem-dev",
        "libqt5x11extras5-dev",
        "qtbase5-dev",
        "qtdeclarative5-dev",
        "qttools5-dev",
    ]
    u.apt_install(
        prerequisites, "hello build prerequisites",
    )
    u.git_clone("https://github.com/Jonchun/hello.git", G["SOURCES_DIR"])

    logger.info("Building window decorations. This can take a while...")
    # "bash build.sh",
    current_file = Path(__file__)
    bash_file = current_file.with_name("{}.sh".format(current_file.stem))
    u.run_shell("bash {}".format(bash_file))

    u.run_shell("cd ~/sources/hello/window-decoration && bash ./build.sh")

    # colors
    hello_light_colors = Path(
        "~/sources/hello/color-scheme/HelloLight.colors"
    ).expanduser()
    hello_dark_colors = Path(
        "~/sources/hello/color-scheme/HelloDark.colors"
    ).expanduser()

    u.cp(hello_light_colors, G["COLOR_SCHEMES_DIR"])
    u.cp(hello_dark_colors, G["COLOR_SCHEMES_DIR"])

    # Plasma Theme
    hello_light_plasma = Path("~/sources/hello/plasma-theme/hellolight").expanduser()

    hello_dark_plasma = Path("~/sources/hello/plasma-theme/hellodark").expanduser()

    u.cp(hello_light_plasma, G["PLASMA_DIR"] / hello_light_plasma.name, "Tr")
    u.cp(hello_dark_plasma, G["PLASMA_DIR"] / hello_dark_plasma.name, "Tr")
