import logging
from pathlib import Path
import select
import subprocess
import shutil
import sys
import urllib.request


logger = logging.getLogger("macifylinux.utils")


def apt_add_ppa(ppa_name):
    # sudo add-apt-repository ppa:krisives/kde-hello
    logger.info("Adding PPA: %s", ppa_name)
    cmd = "sudo add-apt-repository -y ppa:{}".format(ppa_name)
    try:
        run_shell(cmd, stderr_level=logging.DEBUG)
    except subprocess.CalledProcessError:
        logger.error("Unable to add ppa: %s", ppa_name)
        logger.debug("", exc_info=True)


def apt_install(package_names, display_name=None):
    packages = " ".join(package_names)
    if not display_name:
        display_name = package_names
    logger.info("Installing packages: %s", display_name)
    cmd = "sudo apt-get install -y {}".format(packages)
    try:
        run_shell(cmd, stderr_level=logging.DEBUG)
    except subprocess.CalledProcessError:
        logger.error("Unable to install package(s): %s", display_name)
        logger.debug("Package List: %s", packages, exc_info=True)


def change_wallpaper(wallpaper_file):
    with get_template("changeWallpaper.js").open() as f:
        wallpaper_script = f.read()
    wallpaper_script = wallpaper_script.replace("$IMAGE_PATH", str(wallpaper_file))
    eval_plasma_script(wallpaper_script, is_file=False)


def eval_plasma_script(script, is_file=True):
    script_file = script
    # Takes a path object and executes the script
    if is_file:
        with script.open() as f:
            script = f.read()

    try:
        cmd = "dbus-send --session --dest=org.kde.plasmashell --type=method_call /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string:\n{}'".format(
            script
        )
        """
        cmd = "qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript 'string: \n{}'".format(
            script
        )
        """
        subprocess.Popen(cmd, shell=True)
        """

        cmd = 'qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "$(cat {})"'.format(
            script_file
        )
        cmd = [
            "qdbus org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", "$(cat {})"
        ]
        run_shell(cmd)
        """
    except subprocess.CalledProcessError:
        logger.error("Unable to evaluate plasma script: %s", script_file)
        logger.debug("", exc_info=True)


def copy_file(src_file, dest_file, recursive=False):
    if recursive:
        try:
            shutil.copytree(src_file, dest_file)
            return 1
        except FileExistsError:
            shutil.rmtree(dest_file)
            return copy_file(src_file, dest_file, recursive)
    else:
        shutil.copy(src_file, dest_file)
        return 1


def cp(source, dest, flags="", root=False):
    sudo = ""
    if root:
        sudo = "sudo"
    if flags:
        flags = "-{}".format(flags)
    cmd = "{} /bin/cp {} {} {}".format(sudo, flags, source, dest)
    try:
        run_shell(cmd)
    except subprocess.CalledProcessError:
        logger.error("Unable to cp): %s -> %s", source, dest)
        logger.debug("cp flags: %s", flags, exc_info=True)


def download_url(url, target):
    logger.debug("Downloading url: %s", url)
    urllib.request.urlretrieve(url, target)


def get_sudo():
    logger.info(
        "This script will require sudo permissions for certain actions. You may be prompted for your credentials."
    )
    try:
        run_shell("sudo -v")
    except subprocess.CalledProcessError:
        logger.error("Unable to obtain sudo password. Exiting.")
        sys.exit(1)
    # run_shell('sudo -k')


def get_template(template_name):
    template_dir = Path(__file__).parent / Path("templates")
    return template_dir / Path(template_name)


def git_clone(repo_url, target_dir, flags=""):

    cmd = "git -C {} clone {} {}".format(target_dir, flags, repo_url)
    logger.info(cmd)
    logger.info("git cloning %s...", repo_url)
    repo_dir = Path(target_dir) / Path(repo_url).stem
    try:
        run_shell(cmd, stderr_level=logging.DEBUG)
        logger.debug("git clone complete for %s.", repo_url)
        return repo_dir
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            logger.warning("%s already exists! Skipping clone...", repo_url)
            # Should probably git pull instead in the future
            return repo_dir
        logger.error("git clone failed for %s.", repo_url)
        logger.debug("", exc_info=True)
        return False


def install_plasmoid(plasmoid_dir, pretty_name=None):
    if not pretty_name:
        pretty_name = plasmoid_dir.name
    logger.info("Installing Plasmoid: %s", pretty_name)
    cmd = "kpackagetool5 -t Plasma/Applet --install {}".format(plasmoid_dir)
    try:
        run_shell(cmd, stderr_level=logging.DEBUG)
    except subprocess.CalledProcessError as e:
        if "already exists" in e.output:
            logger.warning("Plasmoid is already installed. Skipping: %s", plasmoid_dir)
        else:
            logger.error("Failed while installing plasmoid: %s", plasmoid_dir)
            logger.debug("", exc_info=True)


def kparseconfig(config):
    key = config.get("key")
    value = config.get("value")
    group = config.get("group", "")
    file = config.get("file", "")

    key = "--key {}".format(key)
    if file:
        file = "--file {}".format(file)
    if group:
        if not isinstance(group, list):
            group = [group]
        group_str = " ".join(group)


def kconfig(config, action="", root=False):
    """
    {
        'key': 'key',
        'value': 'value',
        'group': [],
        'file': None
    }
    """
    key = config.get("key")
    value = config.get("value")
    group = config.get("group", "")
    file = config.get("file", "")

    key = "--key {}".format(key)
    if file:
        file = "--file {}".format(file)
    if group:
        if not isinstance(group, list):
            group = [group]
        group = ["--group {}".format(g) for g in group]
        group_str = " ".join(group)

    sudo = "sudo " if root else ""
    if action == "read":
        cmd = "{}kreadconfig5 {} {} {}".format(sudo, file, group_str, key)
    elif action == "write":
        cmd = "{}kwriteconfig5 {} {} {} {}".format(sudo, file, group_str, key, value)
    else:
        raise Exception("Invalid action")

    logger.debug(cmd)

    try:
        return run_shell(cmd, stderr_level=logging.DEBUG)
    except subprocess.CalledProcessError:
        logger.error("Unable to %s with kconfig!", action)
        logger.debug("%s", config, exc_info=True)


def kreadconfig(config, root=False):
    return kconfig(config, action="read", root=root)["stdout"][0]


def kwriteconfig(config, root=False):
    return kconfig(config, action="write", root=root)


def kwriteconfigs(file, configs, root=False):
    # helper utility method to write multiple configs to the same file.
    # configs = list of dicts
    for config in configs:
        config["file"] = file
        kconfig(config, action="write", root=root)


def setup_symlink(source, target, target_is_directory=False):
    """Backs up any existing target to target_bak and then creates a symlink from source to target"""
    if target_is_directory:
        named_target = target / Path(source.name)
        return setup_symlink(source, named_target)
    if target.exists():
        if not target.is_symlink():
            logger.warning("%s already exists. renaming to %s_bak.", target, target)
            target.rename(target.with_name("{}_bak".format(target.name)))
            target.symlink_to(source)
            return True
        target_resolved = str(target.resolve()).replace(str(Path.home()), "~")
        target = str(target).replace(str(Path.home()), "~")
        logger.warning(
            "%s -> %s is already a symlink. Skipping.", target, target_resolved
        )
        return False
    target.symlink_to(source)
    logger.debug("created symlink %s -> %s", source, target)
    return True


def stop_plasma():
    logger.debug("Stopping Plasma.")
    run_shell("kquitapp5 plasmashell")


def start_plasma():
    logger.debug("Starting Plasma.")
    # execute it directly via Popen so that there are no open pipes when program exits.
    subprocess.Popen("kstart5 plasmashell > /dev/null 2>&1", shell=True)


def restart_kwin():
    # execute it directly via Popen so that there are no open pipes when program exits.
    subprocess.Popen("kwin --replace > /dev/null 2>&1", shell=True)


def stop_latte():
    logger.debug("Stopping Latte Dock.")
    try:
        run_shell("killall -9 latte-dock > /dev/null 2>&1")
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            pass
        else:
            logger.error("Problem while trying to stop latte-dock.")
            logger.debug("", exc_info=True)


def start_latte():
    logger.debug("Starting Latte Dock.")
    # execute it directly via Popen so that there are no open pipes when program exits.
    # subprocess.Popen("nohup latte-dock > /dev/null 2>&1 &", shell=True)
    try:
        subprocess.run("nohup latte-dock > /dev/null 2>&1 &", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Problem while starting latte dock: %s", e)
        logger.debug("", exc_info=True)


def run_shell(cmd, stdout_level=logging.DEBUG, stderr_level=logging.ERROR, root=False):
    """
    https://gist.github.com/bgreenlee/1402841
    """
    if root:
        cmd = "sudo {}".format(cmd)
    logger.debug("Running Shell Command: %s", cmd)
    p = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )

    log_level = {p.stdout: stdout_level, p.stderr: stderr_level}
    log_cache = {
        p.stdout: [],
        p.stderr: [],
    }

    def check_io():
        ready = select.select([p.stdout, p.stderr], [], [], 1000)[0]

        for io in ready:
            line = io.readline().strip()
            if not line:
                continue
            logger.log(log_level[io], line[:-1].decode())
            log_cache[io].append(line[:-1].decode())
            """
            lines = io.readlines()
            for line in lines:
                logger.log(log_level[io], line[:-1].decode())
                log_cache[io].append(line[:-1].decode())
            """

    # keep checking stdout/stderr until the child exits
    while p.poll() is None:
        check_io()
    # check again to catch anything after the process exits
    check_io()
    p.wait()

    if p.returncode != 0:
        # https://github.com/python/cpython/blob/c6e5c1123bac6cbb4c85265155af5349dcea522e/Lib/subprocess.py#L114
        output = "\n".join(log_cache[p.stderr]).strip()
        raise subprocess.CalledProcessError(
            p.returncode, cmd, output=output, stderr=p.stderr
        )

    ret_dict = {"stdout": log_cache[p.stdout], "stderr": log_cache[p.stderr]}
    return ret_dict
