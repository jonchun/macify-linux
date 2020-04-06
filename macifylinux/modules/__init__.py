from glob import glob
from importlib import import_module
from pathlib import Path

glob_list = glob("{}/*.py".format(Path(__file__).parent))

__all__ = []
for file in glob_list:
    file = Path(file)
    if file.name == "__init__.py":
        continue
    import_module("macifylinux.modules.{}".format(file.stem))
