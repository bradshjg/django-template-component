import glob
import importlib
import sys
from pathlib import Path

from django.apps import apps


def autodiscover_components():
    dirs = (c.path for c in apps.get_app_configs())
    for directory in dirs:
        for path in glob.iglob(str(Path(directory) / "components" / "**/*.py"), recursive=True):
            _import_component_file(path)


def _import_component_file(module_path):
    module_name = Path(module_path).stem
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
