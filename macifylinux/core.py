import logging
from pathlib import Path
import subprocess

from macifylinux.globals import GLOBALS as G
import macifylinux.modules as m
import macifylinux.utils as u

logger = logging.getLogger("macifylinux")


def configure_logging():
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(levelname)s] %(name)s-%(asctime).19s | %(message)s"
    )
    # create file handler which logs all debug messages
    fh = logging.FileHandler("macifylinux.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # create console handler with a higher log level
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)


def install_prerequisites():
    u.apt_install(
        ["build-essential", "git", "software-properties-common"],
        "General Dependencies",
    )


def run():
    configure_logging()
    u.get_sudo()
    install_prerequisites()

    # Make sure all of the local directories we want to use exist.
    for local_dir in G["LOCAL_DIRS"]:
        local_dir.mkdir(parents=True, exist_ok=True)

    modules = []
    modules.append(m.lookandfeel)
    modules.append(m.plasmoids)
    # albert should be installed after lookandfeel due to icons
    modules.append(m.albert)
    # lattedock should be installed AFTER plasmoids so that they will show up.
    modules.append(m.lattedock)
    modules.append((m.kinto, [], {"style": "light"}))

    for module in modules:
        args = []
        kwargs = {}
        if isinstance(module, tuple):
            args = module[1]
            kwargs = module[2]
            module = module[0]

        pretty_name = module.__doc__
        if not pretty_name:
            pretty_name = module.__name__
        logger.info("Installing module: %s", pretty_name)
        if module.pre(*args, **kwargs):
            module.run(*args, **kwargs)
        else:
            logger.error(
                "Problem while processing prerequisites for: %s", module.__name__
            )

    logger.info("Setup Complete. Please restart your machine.")
