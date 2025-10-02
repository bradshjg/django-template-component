import importlib
import glob
import sys
from pathlib import Path

from django.apps import apps

def autodiscover_components():
    dirs = map(lambda c: c.path, apps.get_app_configs())
    for directory in dirs:
        for path in glob.iglob(str(Path(directory) / "components" / "**/*.py"), recursive=True):
            _import_component_file(path)


def _import_component_file(path):
    MODULE_PATH = path
    MODULE_NAME = Path(path).stem
    spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
