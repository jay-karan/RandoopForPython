import argparse
import inspect
import importlib.util
import random
import string
import sys
from pathlib import Path

def load_module(file_path):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module)
    return module

def get_classes(module):
    return [cls for _, cls in inspect.getmembers(module, predicate=inspect.isclass)]

def get_methods(cls):
    return [m for m in dir(cls) if callable(getattr(cls, m)) and not m.startswith("__")]

def generate_random_primitive(param_type):
    if param_type == int:
        return random.randint(0, 100)
    elif param_type == str:
        return ''.join(random.choices(string.ascii_letters, k=5))
    elif param_type == float:
        return random.uniform(0, 100)
    return None

def randoop_test_generator(classes):
    storage = {}  # Store object instances and outputs
    sequences = []
    error_prone_cases = []

    for _ in range(50):
        cls = random.choice(classes)
        cls_instance = storage.get(cls.__name__, cls()) if random.choice([True, False]) else cls()
        storage[cls.__name__] = cls_instance

        method_name = random.choice(get_methods(cls_instance))
        method = getattr(cls_instance, method_name)
        sig = inspect.signature(method)

        args = []
        for param in sig.parameters.values():
            if param.default is not inspect.Parameter.empty:
                args.append(param.default)
            elif param.annotation in [int, str, float]:
                args.append(generate_random_primitive(param.annotation))
            else:
                # For non-primitive types, use storage or create a new instance
                arg_instance = storage.get(param.annotation.__name__, param.annotation())
                args.append(arg_instance)
                storage[param.annotation.__name__] = arg_instance

        try:
            result = method(*args)
            print(f"Executed {cls.__name__}.{method_name}({args}) -> {result}")
            storage[method_name] = result
            sequences.append((cls_instance, method_name, args, result))
            print(sequences)

        except Exception as e:
            print(f"Error: {cls.__name__}.{method_name}({args}) raised {e}")
            error_prone_cases.append((cls_instance, method_name, args, str(e)))

    return sequences, error_prone_cases

def write_regression_tests(sequences, module_name):
    test_file_name = "regression_tests.py"
    with open(test_file_name, "w") as f:
        f.write("import pytest\n")
        f.write(f"from {module_name} import *\n\n")

        for idx, (cls_instance, method_name, args, result) in enumerate(sequences):
            f.write(f"def test_{method_name}_{idx}():\n")
            f.write(f"    instance = {cls_instance.__class__.__name__}()\n")
            args_str = ", ".join(
                f"{repr(arg) if isinstance(arg, (int, float, str)) else f'{arg.__class__.__name__}()'}"
                for arg in args
            )
            f.write(f"    result = instance.{method_name}({args_str})\n")

            # Add assertions based on result type
            if isinstance(result, (int, float, str)):
                f.write(f"    assert result == {repr(result)}\n\n")
            else:
                # If result is a complex object, instantiate and use specific checks
                f.write(f"    assert isinstance(result, {result.__class__.__name__})\n\n")

    print(f"Regression tests written to {test_file_name}")

def main():
    parser = argparse.ArgumentParser(description="Randoop-style test generator for Python classes")
    parser.add_argument("file", type=str, help="Path to the Python file with class definitions")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.is_file():
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    module = load_module(file_path)
    classes = get_classes(module)

    if not classes:
        print(f"No classes found in '{file_path}'.")
        sys.exit(1)

    sequences, error_prone_cases = randoop_test_generator(classes)

    print("\nSuccessful Sequences:")
    for cls_instance, method_name, args, result in sequences:
        print(f"{cls_instance.__class__.__name__}.{method_name}({args}) -> {result}")

    print("\nError-Prone Sequences:")
    for cls_instance, method_name, args, error in error_prone_cases:
        print(f"{cls_instance.__class__.__name__}.{method_name}({args}) -> Error: {error}")

    write_regression_tests(sequences, module.__name__)

if __name__ == "__main__":
    main()

# import argparse
# import inspect
# import importlib.util
# import random
# import string
# import sys
# from pathlib import Path

# # Utility functions
# def load_module(file_path):
#     spec = importlib.util.spec_from_file_location("module.name", file_path)
#     module = importlib.util.module_from_spec(spec)
#     sys.modules["module.name"] = module
#     spec.loader.exec_module(module)
#     return module

# def get_classes(module):
#     return [cls for _, cls in inspect.getmembers(module, predicate=inspect.isclass)]

# def get_methods(cls):
#     return [m for m in dir(cls) if callable(getattr(cls, m)) and not m.startswith("__")]

# def generate_random_primitive(param_type):
#     if param_type == int:
#         return random.randint(0, 100)
#     elif param_type == str:
#         return ''.join(random.choices(string.ascii_letters, k=5))
#     elif param_type == float:
#         return random.uniform(0, 100)
#     return None

# # Core Randoop-like Algorithm Functions
# def randoop_test_generator(classes):
#     storage = {}  # Stores instances and output values for reuse
#     sequences = []  # Stores successful sequences for regression tests
#     error_prone_cases = []  # Stores sequences with expected errors

#     for _ in range(50):  # Number of random test cases
#         cls = random.choice(classes)
#         cls_instance = storage.get(cls.__name__, cls()) if random.choice([True, False]) else cls()
#         storage[cls.__name__] = cls_instance  # Store instance

#         # Get a random method from the class
#         method_name = random.choice(get_methods(cls_instance))
#         method = getattr(cls_instance, method_name)
#         sig = inspect.signature(method)

#         # Generate arguments
#         args = []
#         for param in sig.parameters.values():
#             if param.annotation in [int, str, float]:
#                 arg = generate_random_primitive(param.annotation)
#             else:
#                 arg = storage.get(param.annotation.__name__, param.annotation())
#             args.append(arg)

#         # Attempt to execute and handle exceptions
#         try:
#             result = method(*args)
#             print(f"Executed {cls.__name__}.{method_name}({args}) -> {result}")
#             # Store result if successful
#             storage[method_name] = result
#             sequences.append((cls_instance, method_name, args, result))

#         except Exception as e:
#             print(f"Error: {cls.__name__}.{method_name}({args}) raised {e}")
#             error_prone_cases.append((cls_instance, method_name, args, str(e)))

#     return sequences, error_prone_cases

# def write_regression_tests(sequences, module_name):
#     test_file_name = "regression_tests.py"
#     with open(test_file_name, "w") as f:
#         f.write("import pytest\n")
#         f.write(f"from {module_name} import *\n\n")

#         for idx, (cls_instance, method_name, args, result) in enumerate(sequences):
#             f.write(f"def test_{method_name}_{idx}():\n")
#             f.write(f"    instance = {cls_instance.__class__.__name__}()\n")
#             args_str = ", ".join(repr(arg) for arg in args)
#             f.write(f"    result = instance.{method_name}({args_str})\n")
#             f.write(f"    assert result == {repr(result)}\n\n")

#     print(f"Regression tests written to {test_file_name}")

# # Main CLI function
# def main():
#     parser = argparse.ArgumentParser(description="Randoop-style test generator for Python classes")
#     parser.add_argument("file", type=str, help="Path to the Python file with class definitions")
#     args = parser.parse_args()

#     file_path = Path(args.file)
#     if not file_path.is_file():
#         print(f"Error: The file '{file_path}' does not exist.")
#         sys.exit(1)

#     module = load_module(file_path)
#     classes = get_classes(module)

#     if not classes:
#         print(f"No classes found in '{file_path}'.")
#         sys.exit(1)

#     # Generate test cases
#     sequences, error_prone_cases = randoop_test_generator(classes)

#     # Output results
#     print("\nSuccessful Sequences:")
#     for cls_instance, method_name, args, result in sequences:
#         print(f"{cls_instance.__class__.__name__}.{method_name}({args}) -> {result}")

#     print("\nError-Prone Sequences:")
#     for cls_instance, method_name, args, error in error_prone_cases:
#         print(f"{cls_instance.__class__.__name__}.{method_name}({args}) -> Error: {error}")

#     # Write regression tests
#     write_regression_tests(sequences, module.__name__)

# if __name__ == "__main__":
#     main()
