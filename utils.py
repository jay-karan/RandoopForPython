import importlib.util
import sys
import pathlib

class FileUtils:
    @staticmethod
    def load_module_from_file(file_path):
        """
        Dynamically load a Python module from the given file path.
        """
        module_name = file_path.stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    
    @staticmethod
    def generate_filepath(path):
        return pathlib.Path(path)