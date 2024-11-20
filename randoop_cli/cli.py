import argparse
import inspect
import importlib.util
import random
import string
import sys
import coverage
import os
from pathlib import Path

def load_module(file_path):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module)
    return module

def get_classes(module):
    return [(name, cls) for name, cls in inspect.getmembers(module, predicate=inspect.isclass)]

def get_methods(cls):
    return [
        m for m in dir(cls)
        if callable(getattr(cls, m)) and not m.startswith("__")
    ]


def generate_random_primitive(param_type, storage=None):
    if param_type == int:
        return random.randint(-100, 100)
    elif param_type == float:
        return random.uniform(-100, 100)
    elif param_type == str:
        return ''.join(random.choices(string.ascii_letters, k=5))
    elif param_type == bool:
        return random.choice([True, False])
    elif param_type == list:
        return [generate_random_primitive(random.choice([int, float, str])) for _ in range(random.randint(1, 5))]
    elif param_type == tuple:
        return tuple(generate_random_primitive(random.choice([int, float, str])) for _ in range(random.randint(1, 5)))
    elif param_type == dict:
        return {
            generate_random_primitive(str): generate_random_primitive(random.choice([int, float, str]))
            for _ in range(random.randint(1, 5))
        }
    elif param_type == set:
        return {generate_random_primitive(random.choice([int, str])) for _ in range(random.randint(1, 5))}
    elif param_type == complex:
        return complex(random.randint(-100, 100), random.randint(-100, 100))
    elif isinstance(param_type, type):
        # Handle user-defined classes
        if storage and param_type.__name__ in storage:
            return random.choice(storage[param_type.__name__])
        else:
            try:
                return param_type()
            except Exception as e:
                print(f"Error: Could not instantiate {param_type.__name__}: {e}")
                return None
    else:
        print(f"Warning: Unknown type {param_type}. Returning None.")
        return None



# Generate a storage data structure for classes
def generate_storage_data_structure(classes):
    storage = {}

    for class_name, class_obj in classes:
        storage[class_name] = {
            "instance": [],
            "methods": {}
        }

        methods = inspect.getmembers(class_obj, predicate=inspect.isfunction)
        for method_name, method_obj in methods:
            signature = inspect.signature(method_obj)
            method_storage = {
                "param": []
            }

            for param_name, param in signature.parameters.items():
                if param_name == "self":
                    continue
                param_type = param.annotation if param.annotation != inspect.Parameter.empty else "unknown"
                method_storage["param"].append({param_type: []})

            storage[class_name]["methods"][method_name] = method_storage

    return storage

def create_instance_of_class(cls):
    """
    Dynamically creates an instance of a class by populating its __init__ parameters with random values.
    """
    try:
        init_signature = inspect.signature(cls.__init__)
        init_params = init_signature.parameters
        # Skip 'self' and generate random values for other parameters
        args = {}
        for param_name, param in init_params.items():
            if param_name in ["self", "args", "kwargs"]:
                continue
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else None
            # Generate random value for the parameter
            if param.default == inspect.Parameter.empty:  # Required parameter
                args[param_name] = generate_random_primitive(param_type)
            else:  # Optional parameter, randomly decide to use default or override
                args[param_name] = (
                    generate_random_primitive(param_type) if random.choice([True, False]) else param.default
                )
        if not args:
            return cls()
        # Instantiate the class with the generated arguments
        return cls(**args)
    except Exception as e:
        print(f"Error creating instance of {cls.__name__}: {e}")
        return None


# Generate random tests for the provided classes
def randoop_test_generator(classes, sequence_number=2):
    storage = generate_storage_data_structure(classes)
    sequences = []
    error_prone_cases = []
    cur_seq = []

    for _ in range(sequence_number):
        cls_name, cls = random.choice(classes)
        cls_instance = (
            random.choice(storage[cls_name]["instance"])
            if storage[cls_name]["instance"] and random.choice([True, False])
            else create_instance_of_class(cls)
        )
        storage[cls_name]["instance"].append(cls_instance)

        method_name = random.choice(list(storage[cls_name]["methods"].keys()))
        method = getattr(cls_instance, method_name)
        sig = inspect.signature(method)
        args = []

        for param in storage[cls_name]["methods"][method_name]["param"]:
            for param_type, data_values in param.items():
                if param_type in [int, str, float]:
                    while True:
                        random_value = generate_random_primitive(param_type)
                        if random_value not in data_values:
                            data_values.append(random_value)
                            args.append(random_value)
                            break
                else:
                    print("Non-Primitive Data Types")
                    args.append(None)
                    # Work to be done.
        print("Storage Data Structure:", storage)
        try:
            result = method(*args)
            print(f"Executed {cls_name}.{method_name}({args}) -> {result}")
            cur_seq.append((cls_name, method_name, args, result))
            sequences.append(cur_seq.copy())
        except Exception as e:
            print(f"Error: {cls_name}.{method_name}({args}) raised {e}")
            if len(cur_seq) > 1 :
                sequences.append(cur_seq.copy())
            error_prone_cases.append(cur_seq + [(cls_name, method_name, args, str(e))])
            cur_seq = []
    return sequences, error_prone_cases, storage

def print_coverage(test_file, actual_file):
    """
    Print coverage data for the actual file while running the test file.
    """
    cov = coverage.Coverage(branch=True, source=[str(Path(actual_file).resolve().parent)])
    cov.start()

    try:
        # Use pytest to run the test file
        import pytest
        pytest.main([test_file])
    finally:
        # Stop and save coverage data
        cov.stop()
        cov.save()

    # Generate a coverage report focused on the actual file
    print(f"\nCoverage for {actual_file} while running {test_file}:\n")
    cov.report([str(Path(actual_file).resolve())])

    # Analyze the actual file for detailed coverage
    _, statements, missing, branches, partial_branches = cov.analysis2(str(Path(actual_file).resolve()))

    # Print detailed coverage
    print(f"Lines covered: {len(statements) - len(missing)}/{len(statements)}")
    print(f"Branches covered: {len(branches) - len(partial_branches)}/{len(branches)}\n")

def write_regression_tests(tot_sequences, module_name, file_path):
    """
    Write regression tests to a file, ensuring proper imports and test generation.
    """
    test_file_name = "regression_tests.py"
    file_stem = Path(file_path).stem  # Get the file name without extension

    with open(test_file_name, "w") as f:
        f.write("import pytest\n")
        f.write(f"from {file_stem} import *\n\n")  # Import using the correct module name

        for sequences in tot_sequences:
            for idx, (cls_name, method_name, args, result) in enumerate(sequences):
                f.write(f"def test_{cls_name}_{method_name}_{idx}():\n")
                f.write(f"    instance = {cls_name}()\n")
                args_str = ", ".join(
                    f"{repr(arg) if isinstance(arg, (int, float, str)) else f'{arg.__class__.__name__}()'}"
                    for arg in args
                )
                f.write(f"    result = instance.{method_name}({args_str})\n")

                # Add assertions based on result type
                if isinstance(result, (int, float, str)):
                    f.write(f"    assert result == {repr(result)}\n\n")
                else:
                    f.write(f"    assert isinstance(result, {result.__class__.__name__})\n\n")
    print(f"Regression tests written to {test_file_name}")
    print_coverage(test_file_name, file_path)


def main():
    parser = argparse.ArgumentParser(description="Randoop-style test generator for Python classes")
    parser.add_argument("-k", type=int, default=2, help="Number of times to extend the sequence (default: 2)")
    parser.add_argument("-f", type=str, required=True, help="Path to the Python file with class definitions")
    #parser.add_argument("sequence_length", type=str, help="Number of times to extend the sequence")
    args = parser.parse_args()

    file_path = Path(args.f)
    if not file_path.is_file():
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    #sequence_length = int(args.sequence_length) if args.sequence_length.isdigit() else 2
    sequence_length = args.k
    module = load_module(file_path)
    classes = get_classes(module)

    if not classes:
        print(f"No classes found in '{file_path}'.")
        sys.exit(1)

    sequences, error_prone_cases, storage = randoop_test_generator(classes, sequence_length)

    print("\nSuccessful Sequences:")
    for sequence in sequences:
        for cls_name, method_name, args, result in sequence:
            print(f"{cls_name}.{method_name}({args}) -> {result}")

    print("\nError-Prone Sequences:")
    for each_error_prone_case in error_prone_cases:
        for cls_name, method_name, args, error in each_error_prone_case:
            print(f"{cls_name}.{method_name}({args}) -> Error: {error}")

    write_regression_tests(sequences, module.__name__, file_path)


if __name__ == "__main__":
    main()
