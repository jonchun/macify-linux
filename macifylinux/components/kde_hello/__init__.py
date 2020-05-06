"""Hello Window Decorations"""
import logging
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

component_name = Path(__file__).parent.name
logger = logging.getLogger("macifylinux.components.{}".format(component_name))

apt_requirements = []
build_requirements = [
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
repo_url = "https://github.com/Jonchun/hello.git"
repo_name = Path(repo_url).stem


def configure(*args, **kwargs):
    style = kwargs.get("style", "light")
    if style == "light":
        color_scheme = "HelloLight"
        plasma_theme = "hellolight"
    elif style == "dark":
        # todo. not tested/working.
        color_scheme = "HelloDark"
        plasma_theme = "hellodark"

    # set plasma theme
    u.kwriteconfig(
        {
            "file": "~/.config/plasmarc",
            "group": "Theme",
            "key": "name",
            "value": plasma_theme,
        }
    )

    # set color scheme
    configs = []
    configs.append(
        {"group": "General", "key": "Name", "value": color_scheme,}
    )
    configs.append(
        {"group": "General", "key": "ColorScheme", "value": color_scheme,}
    )
    u.kwriteconfigs("~/.config/kdeglobals", configs)

    # Style the titlebar buttons to add a little bit of margin on left & make it thinner.
    configs = []
    configs.append(
        {"group": "Windeco", "key": "TitleBarHeightSpin", "value": 1,}
    )
    configs.append(
        {"group": "Windeco", "key": "ButtonMarginSpin", "value": 4,}
    )
    u.kwriteconfigs("~/.config/hellorc", configs)

    # Set the kwinrc to hello
    configs = []
    configs.append(
        {"group": "org.kde.kdecoration2", "key": "library", "value": "org.kde.hello",}
    )
    configs.append(
        {"group": "org.kde.kdecoration2", "key": "theme", "value": "hello",}
    )
    u.kwriteconfigs("~/.config/kwinrc", configs)


def install(*args, **kwargs):
    u.git_clone(repo_url, G["SOURCES_DIR"])
    # run install.sh
    u.bash_action(
        action="install", file=__file__, name=component_name, stderr_level=logging.DEBUG
    )
    configure(*args, **kwargs)


def upgrade(*args, **kwargs):
    install(*args, **kwargs)


def remove(*args, **kwargs):
    # run remove.sh
    u.bash_action(action="remove", file=__file__, name=component_name)
