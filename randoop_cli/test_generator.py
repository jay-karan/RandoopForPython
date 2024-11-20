import inspect
import random
from .data_generation import generate_random_primitive
from .coverage_analysis import print_coverage
from pathlib import Path

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
            method_storage = {"param": []}
            for param_name, param in signature.parameters.items():
                if param_name == "self":
                    continue
                param_type = param.annotation if param.annotation != inspect.Parameter.empty else "unknown"
                method_storage["param"].append({param_type: []})
            storage[class_name]["methods"][method_name] = method_storage
    return storage

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
                    args.append(None)
        try:
            result = method(*args)
            cur_seq.append((cls_name, method_name, args, result))
            sequences.append(cur_seq.copy())
        except Exception as e:
            if len(cur_seq) > 1:
                sequences.append(cur_seq.copy())
            error_prone_cases.append(cur_seq + [(cls_name, method_name, args, str(e))])
            cur_seq = []
    return sequences, error_prone_cases, storage

def write_regression_tests(tot_sequences, module_name, file_path):
    test_file_name = "regression_tests.py"
    file_stem = Path(file_path).stem

    with open(test_file_name, "w") as f:
        f.write("import pytest\n")
        f.write(f"from {file_stem} import *\n\n")

        for sequences in tot_sequences:
            for idx, (cls_name, method_name, args, result) in enumerate(sequences):
                f.write(f"def test_{cls_name}_{method_name}_{idx}():\n")
                f.write(f"    instance = {cls_name}()\n")
                args_str = ", ".join(
                    f"{repr(arg) if isinstance(arg, (int, float, str)) else f'{arg.__class__.__name__}()'}"
                    for arg in args
                )
                f.write(f"    result = instance.{method_name}({args_str})\n")

                if isinstance(result, (int, float, str)):
                    f.write(f"    assert result == {repr(result)}\n\n")
                else:
                    f.write(f"    assert isinstance(result, {result.__class__.__name__})\n\n")
    print(f"Regression tests written to {test_file_name}")
    print_coverage(test_file_name, file_path)
