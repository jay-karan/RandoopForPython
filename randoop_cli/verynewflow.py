import inspect
import importlib.util
import random
import string
import sys
from pathlib import Path


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
        #return "KARAN"
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
    
    for param_name, param in signature.parameters.items():
        if param_name == "self":
            continue
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
        args.append(generate_random_value(param_type, class_map, storage))

    try:
        instance = cls(*args)
        print("Created instance of", qualified_cls_name, "with args:", args)
        return instance
    except Exception as e:
        print("Could not create instance of", qualified_cls_name, ":", e, "\n")
        return None


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
    sequences = []
    error_prone_cases = []
    print("-----> Pre-Creating the Instances for all Classes:")
    # Pre-create instances for all classes
    for cls_name, cls in class_map.items():
        if not storage[cls_name]:
            instance = create_instance(cls, class_map, storage)
            if instance:
                storage[cls_name].append(instance)

    # For each class, perform multiple method calls on the same instance
    for cls_name, cls in class_map.items():
        if storage[cls_name]:
            instance = random.choice(storage[str(cls)])
            print("\n-----> Using instance of", cls_name, ":", instance)

            for _ in range(2):  # Number of method invocations per instance
                method_name, method, args, return_type = None, None, None, None
                try:
                    result = invoke_random_method(instance, class_map, storage)
                    if result is None:
                        continue
                    method_name, method, args, return_type = result
                    result = method(*args)  # Invoke the method
                    print("Called", cls_name + "." + method_name, "(", args, ") ->", result)
                    sequences.append((cls_name, method_name, args, result))

                    if return_type and str(return_type) in class_map:
                        storage[str(return_type)].append(result)
                except Exception as e:
                    print(cls_name + "." + method_name, "(", args, ") raised an exception:", e, "\n")
                    error_prone_cases.append((cls_name, method_name, args, str(e)))
    print("Class Map:", class_map)
    print("Storage Map:", storage)
    return {"storage": storage, "sequences": sequences, "error_cases": error_prone_cases}


def main():
    file_path = Path("BankingApplication.py")  # Adjust to your file name
    if not file_path.is_file():
        print("File not found:", file_path, "\n")
        sys.exit(1)

    module = load_module(file_path)
    classes = get_classes(module)

    if not classes:
        print("No classes found in the module.", "\n")
        sys.exit(1)

    test_results = randoop_test_generator(classes)

    print("\n-----> Generated Instances and Sequences:")
    for seq in test_results["sequences"]:
        print(seq)

    print("\n-----> Error-Prone Test Cases:")
    for error in test_results["error_cases"]:
        print(error)


if __name__ == "__main__":
    main()
