import inspect
import random
from .data_generation import generate_random_primitive
from .coverage_analysis import print_coverage
from pathlib import Path
from rich.console import Console
from rich.progress import Progress

console = Console()

def generate_storage_data_structure(classes):
    """
    Generates a storage data structure for the provided classes.
    The storage contains:
      - Instances of the classes.
      - Metadata about class methods, including their parameters.

    Args:
        classes (list): A list of tuples where each tuple contains a class name and its corresponding class object.

    Returns:
        dict: A dictionary with class names as keys and their respective metadata as values.
    """
    storage = {}
    for class_name, class_obj in classes:
        # Initialize storage for each class
        storage[class_name] = {
            "instance": [],  # List to store instances of the class
            "methods": {}    # Dictionary to store method metadata
        }
        # Retrieve all methods from the class
        methods = inspect.getmembers(class_obj, predicate=inspect.isfunction)
        for method_name, method_obj in methods:
            signature = inspect.signature(method_obj)  # Get the method signature
            method_storage = {"param": []}  # Placeholder for method parameters
            for param_name, param in signature.parameters.items():
                if param_name == "self":
                    continue  # Skip the "self" parameter for instance methods
                param_type = param.annotation if param.annotation != inspect.Parameter.empty else "unknown"
                method_storage["param"].append({param_type: []})  # Store parameter type
            storage[class_name]["methods"][method_name] = method_storage
    return storage

def randoop_test_generator(classes, sequence_number=2):
    """
    Generates Randoop-style test sequences for the given classes.

    Args:
        classes (list): A list of tuples containing class names and class objects.
        sequence_number (int): Number of test sequences to generate.

    Returns:
        tuple: A tuple containing:
            - Successful sequences.
            - Error-prone sequences (sequences causing exceptions).
            - The storage data structure.
    """
    # Prepare the storage structure for classes
    storage = generate_storage_data_structure(classes)
    sequences = []          # List to store successful sequences
    error_prone_cases = []  # List to store error-prone cases
    cur_seq = []            # Current sequence being built

    with Progress(console=console) as progress:
        # Set up a progress bar for sequence generation
        task = progress.add_task("[cyan]Generating sequences...", total=sequence_number)

        for i in range(sequence_number):
            # Randomly select a class and create or reuse an instance
            cls_name, cls = random.choice(classes)
            cls_instance = (
                random.choice(storage[cls_name]["instance"])
                if storage[cls_name]["instance"] and random.choice([True, False])
                else cls()
            )
            storage[cls_name]["instance"].append(cls_instance)  # Save the instance

            # Randomly select a method from the class
            method_name = random.choice(list(storage[cls_name]["methods"].keys()))
            method = getattr(cls_instance, method_name)  # Get the method
            sig = inspect.signature(method)
            args = []  # Prepare arguments for the method

            # Generate arguments based on method parameters
            for param in storage[cls_name]["methods"][method_name]["param"]:
                for param_type, data_values in param.items():
                    if param_type in [int, str, float]:  # Handle primitive types
                        while True:
                            random_value = generate_random_primitive(param_type)
                            if random_value not in data_values:
                                data_values.append(random_value)
                                args.append(random_value)
                                break
                    else:
                        args.append(None)  # Default value for unsupported types

            console.log(f"[green]Processing:[/] {cls_name}.{method_name}({args})")
            try:
                # Attempt to execute the method with generated arguments
                result = method(*args)
                cur_seq.append((cls_name, method_name, args, result))  # Add result to sequence
                sequences.append(cur_seq.copy())  # Save the current sequence
            except Exception as e:
                # Handle exceptions and store error-prone sequences
                if len(cur_seq) > 1:
                    sequences.append(cur_seq.copy())
                error_prone_cases.append(cur_seq + [(cls_name, method_name, args, str(e))])
                cur_seq = []

            progress.update(task, advance=1)  # Update progress

    return sequences, error_prone_cases, storage

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
        for sequences in tot_sequences:
            for idx, (cls_name, method_name, args, result) in enumerate(sequences):
                f.write(f"def test_{cls_name}_{method_name}_{idx}():\n")
                f.write(f"    instance = {cls_name}()\n")
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
