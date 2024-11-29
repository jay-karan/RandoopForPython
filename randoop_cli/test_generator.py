import inspect
import random
from .data_generation import generate_random_primitive
from .coverage_analysis import print_coverage
from pathlib import Path
import string
from rich.console import Console
from rich.progress import Progress

console = Console()

class_name_map = {}

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
def randoop_test_generator(classes, sequence_number=2):
    global class_name_map
    class_map = {str(cls): cls for _, cls in classes}
    storage = {str(cls): [] for _, cls in classes}
    class_name_map = {str(cls): name for name, cls in classes}
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

            for _ in range(sequence_number):  # Number of method invocations per instance
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

    return sequences, error_prone_cases, storage, instance_creation_data



# Write test cases based on generated sequences using pytest
def write_test_cases(sequences, storage, module_name, file_path, instance_creation_data):
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



# # Generate random primitive values or instances for non-primitive types
# def generate_random_value(param_type, class_map, storage):
#     qualified_type_name = str(param_type)
#     if param_type == int:
#         return random.randint(-100, 100)
#     elif param_type == float:
#         return random.uniform(-100, 100)
#     elif param_type == str:
#         return ''.join(random.choices(string.ascii_letters, k=5))
#     elif param_type == bool:
#         return random.choice([True, False])
#     elif qualified_type_name in class_map:
#         if qualified_type_name not in storage or not storage[qualified_type_name]:
#             instance = create_instance(class_map[qualified_type_name], class_map, storage)
#             if instance:
#                 storage[qualified_type_name].append(instance)
#         return random.choice(storage[qualified_type_name])
#     else:
#         print("Unknown parameter type:", param_type, "- Returning None.\n")
#         return None


# # Create an instance of a class with random arguments
# def create_instance(cls, class_map, storage):
#     """
#     Generates a storage data structure for the provided classes.
#     The storage contains:
#       - Instances of the classes.
#       - Metadata about class methods, including their parameters.

#     Args:
#         classes (list): A list of tuples where each tuple contains a class name and its corresponding class object.

#     Returns:
#         dict: A dictionary with class names as keys and their respective metadata as values.
#     """
#     qualified_cls_name = str(cls)
#     signature = inspect.signature(cls.__init__)
#     args = []

#     for param_name, param in signature.parameters.items():
#         if param_name == "self":
#             continue
#         param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
#         args.append(generate_random_value(param_type, class_map, storage))

#     try:
#         instance = cls(*args)
#         print("Created instance of", qualified_cls_name, "with args:", args)
#         return instance
#     except Exception as e:
#         print("Could not create instance of", qualified_cls_name, ":", e, "\n")
#         return None


# # Invoke a random method with random arguments on a class instance
# def invoke_random_method(instance, class_map, storage):
#     methods = [
#         m for m in dir(instance)
#         if callable(getattr(instance, m)) and not m.startswith("__")
#     ]

#     if not methods:
#         print("No callable methods found for instance of", type(instance).__name__)
#         return None

#     method_name = random.choice(methods)
#     method = getattr(instance, method_name)
#     signature = inspect.signature(method)
#     args = []

#     for param_name, param in signature.parameters.items():
#         if param_name == "self":
#             continue
#         param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
#         args.append(generate_random_value(param_type, class_map, storage))

#     return_type = signature.return_annotation if signature.return_annotation != inspect.Signature.empty else None
#     print("Preparing to call method:", method_name, "with args:", args)
#     return method_name, method, args, return_type


# # Generate random tests for classes with multiple method calls per instance
# def randoop_test_generator(classes, sequence_number=2):
#     class_map = {str(cls): cls for _, cls in classes}
#     storage = {str(cls): [] for _, cls in classes}
#     sequences = []
#     error_prone_cases = []
#     print("-----> Pre-Creating the Instances for all Classes:")
#     # Pre-create instances for all classes
#     for cls_name, cls in class_map.items():
#         if not storage[cls_name]:
#             instance = create_instance(cls, class_map, storage)
#             if instance:
#                 storage[cls_name].append(instance)

#     with Progress(console=console) as progress:
#         # Set up a progress bar for sequence generation
#         task = progress.add_task("[cyan]Generating sequences...", total=sequence_number)
#         # For each class, perform multiple method calls on the same instance
#         for cls_name, cls in class_map.items():
#             if storage[cls_name]:
#                 instance = random.choice(storage[str(cls)])
#                 print("\n-----> Using instance of", cls_name, ":", instance)

#                 for _ in range(sequence_number):  # Number of method invocations per instance
#                     method_name, method, args, return_type = None, None, None, None
#                     console.log(f"[green]Processing:[/] {cls_name}.{method_name}({args})")
#                     try:
#                         result = invoke_random_method(instance, class_map, storage)
#                         if result is None:
#                             continue
#                         method_name, method, args, return_type = result
#                         result = method(*args)  # Invoke the method
#                         print("Called", cls_name + "." + method_name, "(", args, ") ->", result)
#                         sequences.append((cls_name, method_name, args, result))

#                         if return_type and str(return_type) in class_map:
#                             storage[str(return_type)].append(result)
#                     except Exception as e:
#                         print(cls_name + "." + method_name, "(", args, ") raised an exception:", e, "\n")
#                         error_prone_cases.append((cls_name, method_name, args, str(e)))
#                     progress.update(task, advance=1)  # Update progress
#     print("Class Map:", class_map)
#     print("Storage Map:", storage)
#     return {"storage": storage, "sequences": sequences, "error_cases": error_prone_cases}


# def randoop_test_generator(classes, sequence_number=2):

#     # Prepare the storage structure for classes
#     storage = generate_storage_data_structure(classes)
#     sequences = []          # List to store successful sequences
#     error_prone_cases = []  # List to store error-prone cases
#     cur_seq = []            # Current sequence being built

#     with Progress(console=console) as progress:
#         # Set up a progress bar for sequence generation
#         task = progress.add_task("[cyan]Generating sequences...", total=sequence_number)

#         for i in range(sequence_number):
#             # Randomly select a class and create or reuse an instance
#             cls_name, cls = random.choice(classes)
#             cls_instance = (
#                 random.choice(storage[cls_name]["instance"])
#                 if storage[cls_name]["instance"] and random.choice([True, False])
#                 else cls()
#             )
#             storage[cls_name]["instance"].append(cls_instance)  # Save the instance

#             # Randomly select a method from the class
#             method_name = random.choice(list(storage[cls_name]["methods"].keys()))
#             method = getattr(cls_instance, method_name)  # Get the method
#             sig = inspect.signature(method)
#             args = []  # Prepare arguments for the method

#             # Generate arguments based on method parameters
#             for param in storage[cls_name]["methods"][method_name]["param"]:
#                 for param_type, data_values in param.items():
#                     if param_type in [int, str, float]:  # Handle primitive types
#                         while True:
#                             random_value = generate_random_primitive(param_type)
#                             if random_value not in data_values:
#                                 data_values.append(random_value)
#                                 args.append(random_value)
#                                 break
#                     else:
#                         args.append(None)  # Default value for unsupported types

#             console.log(f"[green]Processing:[/] {cls_name}.{method_name}({args})")
#             try:
#                 # Attempt to execute the method with generated arguments
#                 result = method(*args)
#                 cur_seq.append((cls_name, method_name, args, result))  # Add result to sequence
#                 sequences.append(cur_seq.copy())  # Save the current sequence
#             except Exception as e:
#                 # Handle exceptions and store error-prone sequences
#                 if len(cur_seq) > 1:
#                     sequences.append(cur_seq.copy())
#                 error_prone_cases.append(cur_seq + [(cls_name, method_name, args, str(e))])
#                 cur_seq = []

#             progress.update(task, advance=1)  # Update progress

#     return sequences, error_prone_cases, storage

def write_regression_tests(tot_sequences, module_name, file_path):
    """
    Writes generated test sequences to a regression test file.

    Args:
        tot_sequences (list): List of successful test sequences.
        module_name (str): Name of the module containing the classes.
        file_path (Path): Path to the file with class definitions.
    """
    test_file_name = "regression_tests.py"
    file_stem = Path(file_path).stem  # Get the file name without extension

    with open(test_file_name, "w") as f:
        # Write imports for the test file
        f.write("import pytest\n")
        f.write(f"from {file_stem} import *\n\n")

        # Generate test functions for each sequence
        for id, sequences in enumerate(tot_sequences):
            f.write(f"def test_{sequences[0][0]}_{sequences[0][1]}_{id}():\n")
            f.write(f"    instance = {sequences[0][0]}()\n")
            for idx, (cls_name, method_name, args, result) in enumerate(sequences):
                args_str = ", ".join(
                    f"{repr(arg) if isinstance(arg, (int, float, str)) else f'{arg.__class__.__name__}()'}"
                    for arg in args
                )
                f.write(f"    result = instance.{method_name}({args_str})\n")

                # Write assertions based on result types
                if isinstance(result, (int, float, str)):
                    f.write(f"    assert result == {repr(result)}\n\n")
                else:
                    f.write(f"    assert isinstance(result, {result.__class__.__name__})\n\n")
    # Notify the user of the generated test file
    console.print(f"[bold green]Regression tests written to {test_file_name}[/bold green]")
    print_coverage(test_file_name, file_path)
