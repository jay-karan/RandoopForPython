import inspect
import importlib.util
import sys
import pathlib
from utils import FileUtils

def inspect_classes(module):
    classes = [cls for _, cls in inspect.getmembers(module, predicate=inspect.isclass)]
    print(f"Found {len(classes)} class(es) in module '{module.__name__}':")

    return classes

def inspect_methods(classes, module):
    print(classes)
    class_methods = {}
    for cls in classes:
        print(f"\nClass: {cls.__name__}")
        methods = [m for m in inspect.getmembers(cls, predicate=inspect.isfunction) if not m[0].startswith('__')]
        print(f"  Number of methods: {len(methods)}")
        if cls not in class_methods:
            class_methods[cls] = [methods]
        for name, method in methods:
            print(f"  Method: {name}, Signature: {inspect.signature(method)}")
    return class_methods

def inspect_classes_and_methods(module):
    """
    Inspects all classes in a given module and their methods.
    """
    classes = [cls for _, cls in inspect.getmembers(module, predicate=inspect.isclass)]
    print(f"Found {len(classes)} class(es) in module '{module.__name__}':")
    
    for cls in classes:
        print(f"\nClass: {cls.__name__}")
        methods = [m for m in inspect.getmembers(cls, predicate=inspect.isfunction) if not m[0].startswith('__')]
        print(f"  Number of methods: {len(methods)}")
        
        for name, method in methods:
            print(f"  Method: {name}, Signature: {inspect.signature(method)}")

if __name__ == "__main__":
    file_path = FileUtils.generate_filepath('class_definitions.py')
    if not file_path.is_file():
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)
    module = FileUtils.load_module_from_file(file_path)
 
    classes = inspect_classes(module)
    if not classes:
        print(f"Error: The file '{file_path}' does not have any valid classes.")
        sys.exit(1)
      
    class_methods = inspect_methods(classes, module)

    #inspect_classes_and_methods(module)
