"""This module is responsible for all of the theming/fonts/icons"""
import logging
from pathlib import Path
import subprocess
import tempfile

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
    u.cp(mcmojave_cursors, G["ICONS_DIR"] / Path("McMojave-cursors"), "r")


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
        u.run_shell('rm -rf {}'. format(theme_path), root=True)

    u.cp(kde_plasma_chili, theme_path, flags="r", root=True)

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
    u.apt_add_ppa("krisives/kde-hello")
    u.apt_install(["kde-hello"], "kde-hello window decorations")
