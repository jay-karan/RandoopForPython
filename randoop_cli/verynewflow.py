import inspect
import importlib.util
import random
import string
import sys
from pathlib import Path

class_name_map = {}
# Load a Python module dynamically
def load_module(file_path):
    print("\nLoading module from:", file_path)
    try:
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = module
        spec.loader.exec_module(module)
        print("Module loaded successfully from:", file_path, "\n")
        return module
    except Exception as e:
        print("Failed to load module:", e, "\n")
        sys.exit(1)


# Get all classes from a module
def get_classes(module):
    classes = [(name, cls) for name, cls in inspect.getmembers(module, predicate=inspect.isclass)]
    print("Found", len(classes), "classes:", [name for name, _ in classes], "\n")
    return classes


# Generate random primitive values or instances for non-primitive types
def generate_random_value(param_type, class_map, storage):
    qualified_type_name = str(param_type)
    if param_type == int:
        return random.randint(-100, 100)
    elif param_type == float:
        return random.uniform(-100, 100)
    elif param_type == str:
        return ''.join(random.choices(string.ascii_letters, k=5))
    elif param_type == bool:
        return random.choice([True, False])
    elif qualified_type_name in class_map:
        if qualified_type_name not in storage or not storage[qualified_type_name]:
            instance = create_instance(class_map[qualified_type_name], class_map, storage)
            if instance:
                storage[qualified_type_name].append(instance)
        return random.choice(storage[qualified_type_name])
    else:
        print("Unknown parameter type:", param_type, "- Returning None.\n")
        return None


# Create an instance of a class with random arguments
def create_instance(cls, class_map, storage):
    qualified_cls_name = str(cls)
    signature = inspect.signature(cls.__init__)
    args = []
    instance_data = {}

    for param_name, param in signature.parameters.items():
        if param_name == "self":
            continue
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
        args.append(generate_random_value(param_type, class_map, storage))

    try:
        instance = cls(*args)
        instance_id = f"{class_name_map.get(qualified_cls_name, qualified_cls_name)}_{len(storage[qualified_cls_name]) + 1}"
        instance_data = {
            "id": instance_id,
            "class": qualified_cls_name,
            "args": args
        }
        print(f"Created instance {instance_id} of {qualified_cls_name} with args: {args}")
        return instance, instance_data
    except Exception as e:
        print(f"Could not create instance of {qualified_cls_name}: {e}\n")
        return None, instance_data


# Invoke a random method with random arguments on a class instance
def invoke_random_method(instance, class_map, storage):
    methods = [
        m for m in dir(instance)
        if callable(getattr(instance, m)) and not m.startswith("__")
    ]

    if not methods:
        print("No callable methods found for instance of", type(instance).__name__)
        return None

    method_name = random.choice(methods)
    method = getattr(instance, method_name)
    signature = inspect.signature(method)
    args = []

    for param_name, param in signature.parameters.items():
        if param_name == "self":
            continue
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
        args.append(generate_random_value(param_type, class_map, storage))

    return_type = signature.return_annotation if signature.return_annotation != inspect.Signature.empty else None
    print("Preparing to call method:", method_name, "with args:", args)
    return method_name, method, args, return_type


# Generate random tests for classes with multiple method calls per instance
def randoop_test_generator(classes):
    class_map = {str(cls): cls for _, cls in classes}
    storage = {str(cls): [] for _, cls in classes}
    instance_creation_data = {}
    sequences = []
    error_prone_cases = []

    print("-----> Pre-Creating the Instances for all Classes:")
    # Pre-create instances for all classes
    for cls_name, cls in class_map.items():
        if not storage[cls_name]:
            instance, instance_data = create_instance(cls, class_map, storage)
            print(instance, instance_data)
            if instance:
                storage[cls_name].append(instance)
                instance_creation_data[instance_data["id"]] = instance_data

    # For each class, perform multiple method calls on the same instance
    for cls_name, cls in class_map.items():
        if storage[cls_name]:
            instance = random.choice(storage[cls_name])
            print("\n-----> Using instance of", cls_name, ":", instance)

            for _ in range(12):  # Number of method invocations per instance
                method_name, method, args, return_type = None, None, None, None
                try:
                    result = invoke_random_method(instance, class_map, storage)
                    if result is None:
                        continue
                    method_name, method, args, return_type = result
                    result = method(*args)  # Invoke the method
                    print("Called", cls_name + "." + method_name, "(", args, ") ->", result)

                    instance_id = instance_creation_data.get(f"{class_name_map[cls_name]}_{len(storage[cls_name])}", {}).get("id", "")
                    sequences.append({
                        "instance_id": instance_id,
                        "class_name": cls_name,
                        "method_name": method_name,
                        "args": args,
                        "result": result,
                        "return_type": return_type
                    })

                    if return_type and str(return_type) in class_map:
                        storage[str(return_type)].append(result)
                except Exception as e:
                    print(cls_name + "." + method_name, "(", args, ") raised an exception:", e, "\n")
                    error_prone_cases.append((cls_name, method_name, args, str(e)))

    return {"storage": storage, "sequences": sequences, "error_cases": error_prone_cases, "instance_creation_data": instance_creation_data}


# Write test cases based on generated sequences using pytest
def write_test_cases(sequences, storage, module_name, file_path, class_name_map, instance_creation_data):
    """
    Writes the generated test cases to a pytest-compatible file.
    """
    test_file_name = "generated_test_cases.py"
    file_stem = Path(file_path).stem

    with open(test_file_name, "w") as f:
        f.write("import pytest\n")
        f.write(f"from {file_stem} import *\n\n")

        # Write instance initialization code
        f.write("# Initialize instances\n")
        for instance_id, instance_data in instance_creation_data.items():
            cls_name = class_name_map[instance_data["class"]]
            args = instance_data["args"]
            print(cls_name, args)
            args_str = ", ".join(
                f"{repr(arg) if isinstance(arg, (int, float, str, bool)) else arg.__class__.__name__ + '()'}"
                for arg in args
            )
            f.write(f"{instance_id} = {cls_name}({args_str})\n")
        f.write("\n")
        print("TEST CASE GENERATION ")
        # Write test cases
        f.write("# Test cases\n")
        for idx, seq in enumerate(sequences):
            print(seq)
            instance_id = seq["instance_id"]
            class_name = class_name_map[seq["class_name"]]
            method_name = seq["method_name"]
            args = seq["args"]
            result = seq["result"]

            f.write(f"def test_{class_name}_{method_name}_{idx}():\n")
            f.write(f"    instance = {instance_id}\n")
            args_str = ", ".join(
                f"{repr(arg) if isinstance(arg, (int, float, str, bool)) else f'{arg.__class__.__name__}()'}"
                for arg in args
            )
            f.write(f"    result = instance.{method_name}({args_str})\n")

            if isinstance(result, (int, float, str, bool)):
                f.write(f"    assert result == {repr(result)}\n\n")
            else:
                f.write(f"    assert isinstance(result, {result.__class__.__name__})\n\n")


def main():
    global class_name_map
    fileName = "EmployeeApplication.py"
    file_path = Path(fileName)  # Adjust to your file name
    if not file_path.is_file():
        print("File not found:", file_path, "\n")
        sys.exit(1)

    module = load_module(file_path)
    classes = get_classes(module)
    class_name_map = {str(cls): name for name, cls in classes}

    if not classes:
        print("No classes found in the module.\n")
        sys.exit(1)

    # Generate random tests
    test_results = randoop_test_generator(classes)

    # Write the tests to a file
    write_test_cases(test_results["sequences"], test_results["storage"], module.__name__,
                     file_path, class_name_map, test_results["instance_creation_data"])


if __name__ == "__main__":
    main()
