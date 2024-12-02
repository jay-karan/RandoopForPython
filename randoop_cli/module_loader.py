import importlib.util
import sys

def load_module(file_path, shared_namespace, console):
    """
    Dynamically load a Python module from a file and add its contents to the shared namespace.
    
    Args:
        file_path (Path): Path to the Python file.
        shared_namespace (dict): Dictionary to store shared symbols across modules.
        console (Console): Rich Console instance for logging.

    Returns:
        module: The loaded Python module.
    """
    module_name = file_path.stem  # Use the file's stem as the module name
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  # Add to sys.modules using the file's stem
    try:
        spec.loader.exec_module(module)
        shared_namespace.update(vars(module))  # Merge module symbols into shared namespace
        console.print(f"[bold green]Successfully loaded module: {file_path}[/bold green]")
        return module
    except Exception as e:
        console.print(f"[bold red]Error loading module {file_path}: {e}[/bold red]")
        raise
