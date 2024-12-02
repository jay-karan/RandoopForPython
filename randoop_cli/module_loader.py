import importlib.util
import sys
import os

def load_module(file_path, namespace):
    """
    Load a Python module from a file path into a shared namespace.
    Skip setup.py or files that shouldn't be loaded.
    """
    # Skip setup.py as it causes issues during package loading
    if file_path.name == "setup.py":
        print(f"Skipping {file_path} due to potential issues with loading")
        return

    module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    spec.loader.exec_module(module)

    # Merge module attributes into the shared namespace
    for name, obj in vars(module).items():
        if not name.startswith("_"):  # Ignore private attributes
            namespace[name] = obj

    return module
