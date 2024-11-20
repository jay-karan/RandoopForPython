### Randoop-Style Test Generator for Python Classes

---

#### **Overview**

This project implements a Python-based tool for generating **Randoop-style tests**. Randoop is a unit test generation framework that automatically creates test cases by exploring possible sequences of method invocations for classes. This project aims to replicate the core functionality of Randoop by generating sequences of method calls for Python classes, handling edge cases, and writing regression tests for successful test sequences.

With features like **dynamic method inspection**, **random data generation**, and **error handling for invalid cases**, this tool is ideal for automating the testing process in Python.

---

### **Features**

- **Automatic Method Inspection**: Dynamically inspects and identifies all methods within a class, including their parameters.
- **Randomized Test Generation**: Generates sequences of method calls with randomly generated valid arguments.
- **Error-Prone Case Logging**: Captures method invocations that result in exceptions and logs them for further debugging.
- **Regression Test Generation**: Automatically writes successful test cases to a file in `pytest` format for reuse.
- **Rich CLI Interface**: A visually appealing command-line interface built with the `rich` library, including progress bars and logs.
- **Supports Custom Data Types**: Extensible to handle custom parameter types or annotations.

---

### **How It Works**

#### **Methods Overview**

1. **`generate_storage_data_structure(classes)`**
   - **Purpose**: Creates a structured representation of the classes and their methods.
   - **How It Works**:
     - Inspects methods of all classes.
     - Stores method signatures and parameter types.
     - Initializes an empty storage for instances and test data.
   - **Output**: A dictionary mapping class names to their metadata.

2. **`randoop_test_generator(classes, sequence_number=2)`**
   - **Purpose**: Generates sequences of method calls for the provided classes.
   - **How It Works**:
     - Randomly selects a class and method.
     - Generates random arguments for the method based on its signature.
     - Invokes the method and stores results or exceptions.
     - Updates a progress bar for better user experience.
   - **Output**:
     - **Successful sequences**: Valid test cases.
     - **Error-prone cases**: Methods that threw exceptions.
     - **Updated storage**: Includes instances and parameter values.

3. **`write_regression_tests(tot_sequences, module_name, file_path)`**
   - **Purpose**: Writes the generated sequences as regression tests in `pytest` format.
   - **How It Works**:
     - Iterates through successful sequences.
     - Generates Python test functions with proper assertions.
     - Saves the tests to a `regression_tests.py` file.
   - **Output**: A reusable regression test file.

---

### **How to Run**

#### **Requirements**

Ensure you have the following Python packages installed:

```bash
pip install rich tqdm pytest
```

#### **Steps to Run**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jay-karan/RandoopForPython.git
   cd RandoopForPython
   ```

2. **Prepare Your Python Module**:
   Place the Python file containing your classes in the same directory (e.g., `example_classes.py`).

3. **Run the Tool**:
   ```bash
   python test_generator_cli.py -f <path-to-python-file> -k <sequence-length>
   ```

   - **`-f`**: Path to the Python file containing class definitions.
   - **`-k`**: Number of test sequences to generate (default is `2`).

4. **Output**:
   - Generated test sequences and their outcomes are displayed in the console.
   - Regression tests are saved in `regression_tests.py`.

#### **Example**

```bash
python test_generator_cli.py -f example_classes.py -k 3
```

---

### **Installation and Usage with CLI**

This project provides a convenient command-line interface (CLI) for generating Randoop-style tests, simplifying the workflow. Follow these steps to install and use the CLI:

---

#### **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jay-karan/RandoopForPython.git
   cd RandoopForPython
   ```

2. **Install as a Python Package**:
   Run the following command to install the project as a Python package:
   ```bash
   pip install .
   ```

   This will make the CLI tool available globally as `randoop-cli`.

---

#### **Usage**

Once installed, you can use the CLI to generate Randoop-style tests with a simple command:

```bash
randoop-cli -f <path-to-python-file> -k <sequence-length>
```

- **`-f`**: Path to the Python file containing the class definitions.
- **`-k`**: (Optional) Number of test sequences to generate (default: `2`).

---

#### **Examples**

1. **Basic Usage**:
   ```bash
   randoop-cli -f example_classes.py
   ```
   This generates test sequences for the `example_classes.py` file with the default sequence length of 2.

2. **Specify Sequence Length**:
   ```bash
   randoop-cli -f example_classes.py -k 5
   ```
   This generates 5 test sequences.

---

#### **Output**

- **Test Results**:
  - Displays successful and error-prone sequences in the terminal.

- **Regression Tests**:
  - A `regression_tests.py` file is created in the working directory, containing reusable `pytest` test cases for the successful sequences.

---

### **Benefits of CLI Installation**

- **Global Access**: No need to navigate to the project directory every time—run the tool from anywhere.
- **Streamlined Workflow**: Simplified command structure for efficient testing.

With the CLI installed, integrating Randoop-style test generation into your development workflow becomes effortless! 🚀

---

### **Supported Functionality**

- **Dynamic Class Inspection**: Supports any Python class with methods.
- **Primitive Data Types**: Handles `int`, `float`, and `str` parameters.
- **Custom Classes**: Placeholder support for custom parameter types (returns `None`).

---

### **Future Enhancements**

1. **Support for Complex Data Types**:
   - Add support for lists, dictionaries, and user-defined types in method parameters.

2. **Enhanced Random Value Generation**:
   - Integrate libraries like `faker` for richer and more realistic test data.

3. **Improved Error Handling**:
   - Add detailed stack traces for error-prone cases.

4. **Sequence Optimization**:
   - Implement smarter test generation strategies to cover edge cases efficiently.

5. **Test Coverage Analysis**:
   - Include a built-in module for measuring code coverage of generated tests.

6. **GUI Support**:
   - Add a graphical user interface for easier usage and configuration.

---

### **Project Structure**

```plaintext
.
├── data_generation.py          # Module for generating random primitive values.
├── coverage_analysis.py        # Module for analyzing test coverage.
├── test_generator.py           # Core logic for test generation and regression test writing.
├── cli.py                      # Command-line interface for running the tool.
├── module_loader.py            # Command-line interface for running the tool.
├── regression_tests.py         # Automatically generated regression tests.
```

---

### **Contributing**

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your fork and submit a pull request.

---

### **License**

This project is licensed under the MIT License.

---

### **Contact**

For questions or feedback, feel free to reach out by creating issues.

---
Happy Coding 🚀
