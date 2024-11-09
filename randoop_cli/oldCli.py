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

def generate_random_input(param_type):
    if param_type == int:
        return random.randint(0, 100)
    elif param_type == str:
        return ''.join(random.choices(string.ascii_letters, k=5))
    elif param_type == float:
        return random.uniform(0, 100)
    return None

def generate_test_cases(cls_instance):
    test_cases = []
    previous_outputs = {}

    for method_name in get_methods(cls_instance):
        method = getattr(cls_instance, method_name)
        sig = inspect.signature(method)
        params = []

        for param in sig.parameters.values():
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
            if param_type in previous_outputs:
                params.append(previous_outputs[param_type])
            else:
                input_val = generate_random_input(param_type)
                previous_outputs[param_type] = input_val
                params.append(input_val)

        test_cases.append((method_name, params))
    return test_cases

def execute_test_cases(cls_instance, test_cases):
    results = []
    for method_name, args in test_cases:
        method = getattr(cls_instance, method_name)
        try:
            result = method(*args)
            results.append((method_name, args, result, type(result)))
        except Exception as e:
            results.append((method_name, args, None, str(e)))
    return results

def write_test_cases_to_file(cls, test_cases, module_name):
    test_file_name = f"test_{cls.__name__.lower()}.py"
    with open(test_file_name, "w") as f:
        f.write("import pytest\n")
        f.write(f"from {module_name} import {cls.__name__}\n\n")

        for idx, (method_name, args) in enumerate(test_cases):
            f.write(f"def test_{method_name}_{idx}():\n")
            f.write(f"    instance = {cls.__name__}()\n")
            args_str = ", ".join(repr(arg) for arg in args)
            f.write(f"    result = instance.{method_name}({args_str})\n")
            f.write(f"    assert result is not None  # Customize this assertion as needed\n\n")

    print(f"Test cases written to {test_file_name}")

def main():
    parser = argparse.ArgumentParser(description="Randoop-style test generator for Python classes")
    parser.add_argument("file", type=str, help="Path to the Python file with class definitions")
    args = parser.parse_args()

    # Load module and inspect classes
    file_path = Path(args.file)
    if not file_path.is_file():
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    module = load_module(file_path)
    classes = get_classes(module)

    if not classes:
        print(f"No classes found in '{file_path}'.")
        sys.exit(1)

    # Process each class found in the module
    for cls in classes:
        print(f"\nGenerating test cases for class '{cls.__name__}'")
        cls_instance = cls()
        test_cases = generate_test_cases(cls_instance)

        # Execute test cases
        results = execute_test_cases(cls_instance, test_cases)
        for method_name, args, result, result_type in results:
            print(f"Method: {method_name} | Args: {args} | Result: {result} | Type: {result_type}")

        # Write test cases to a file
        write_test_cases_to_file(cls, test_cases, module.__name__)

if __name__ == "__main__":
    main()
