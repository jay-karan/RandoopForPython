import argparse
from pathlib import Path
from .module_loader import load_module
from .class_inspection import get_classes
from .test_generator import randoop_test_generator, write_regression_tests
import sys
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
