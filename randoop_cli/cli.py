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
            else cls()
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
def write_regression_tests(tot_sequences, module_name):
    test_file_name = "regression_tests.py"
    with open(test_file_name, "w") as f:
        f.write("import pytest\n")
        f.write(f"from {module_name} import *\n\n")
        for sequences in tot_sequences:
            print("SEquence ", sequences)
            for idx, (cls_name, method_name, args, result) in enumerate(sequences):
                f.write(f"def test_{method_name}_{idx}():\n")
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

def main():
    parser = argparse.ArgumentParser(description="Randoop-style test generator for Python classes")
    parser.add_argument("file", type=str, help="Path to the Python file with class definitions")
    parser.add_argument("sequence_length", type=str, help="Number of Time the Sequence must be tried to extend")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.is_file():
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)
    sequence_length = int(args.sequence_length)
    if not sequence_length:
        sequence_length = 2
    print("Seq Len", sequence_length)

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
    for each_error_prone_cases in error_prone_cases:
        for cls_name, method_name, args, error in each_error_prone_cases:
            print(f"{cls_name}.{method_name}({args}) -> Error: {error}")

    write_regression_tests(sequences, module.__name__)

if __name__ == "__main__":
    main()
