"""Look and Feel packages"""
from pathlib import Path

from macifylinux.globals import GLOBALS as G
import macifylinux.utils as u

from .configure import configure
from .install import install


def pre(*args, **kwargs):
    setup_dirs()
    return True


def run(*args, **kwargs):
    install(*args, **kwargs)
    configure(*args, **kwargs)
    return True


def setup_dirs():
    """Set up the initial directory structure
    Our goal is to have the following:
    ~/.icons -> ~/.local/share/icons
    ~/.fonts -> ~/.local/share/fonts

    Also want to make sure all of the target local dirs exist.
    """
    dot_icons_dir = Path("~/.icons").expanduser()
    u.setup_symlink(G["ICONS_DIR"], dot_icons_dir)

    dot_fonts_dir = Path("~/.fonts").expanduser()
    u.setup_symlink(G["FONTS_DIR"], dot_fonts_dir)
