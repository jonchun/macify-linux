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
    logger.info(
        "Only basic information will be output on screen. To see full debug logs, you can tail -f macifylinux.log."
    )
    install_prerequisites()

    # Make sure all of the local directories we want to use exist.
    for local_dir in G["LOCAL_DIRS"]:
        local_dir.mkdir(parents=True, exist_ok=True)

    modules = []
    # install Kinto(hotkeys module) first because it requires user interaction.
    modules.append(m.hotkeys)
    # modules.append((m.lookandfeel, [], {"style": "light"}))
    modules.append(m.lookandfeel)
    # spotlight should be installed after lookandfeel because it needs access to the installed icons
    modules.append(m.spotlight)
    modules.append(m.plasmoids)
    # dockandpanel should be installed AFTER plasmoids because latte-dock depends on the installed plasmoids.
    modules.append(m.dockandpanel)

    for module in modules:
        args = []
        kwargs = {}
        if isinstance(module, tuple):
            module, args, kwargs = module

        pretty_name = module.__doc__
        if not pretty_name:
            pretty_name = module.__name__
        logger.info("Installing module: %s", pretty_name)
        module_reqs = u.get_module_requirements(module)
        logger.debug("%s", module_reqs)
        u.apt_install(module_reqs, "{} requirements".format(pretty_name))
        module.install(*args, **kwargs)

        # if module.pre(*args, **kwargs):
        #     module.run(*args, **kwargs)
        # else:
        #     logger.error(
        #         "Problem while processing prerequisites for: %s", module.__name__
        #     )

    logger.info("Setup Complete. Please restart your machine.")
