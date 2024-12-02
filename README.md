# **Randoop-Style Test Generator for Python Classes**

## **Overview**

This project implements a Python-based tool for generating **Randoop-style tests**. Randoop is a unit test generation framework that automatically creates test cases by exploring possible sequences of method invocations for classes. This project aims to replicate the core functionality of Randoop by generating sequences of method calls for Python classes, handling edge cases, and writing regression tests for successful test sequences.

With features like **dynamic method inspection**, **random data generation**, and **error handling for invalid cases**, this tool is ideal for automating the testing process in Python.

---

## **Features**

- **Automatic Method Inspection**: Dynamically inspects and identifies all methods within a class, including their parameters.
- **Randomized Test Generation**: Generates sequences of method calls with randomly generated valid arguments.
- **Error-Prone Case Logging**: Captures method invocations that result in exceptions and logs them for further debugging.
- **Regression Test Generation**: Automatically writes successful test cases to a file in `pytest` format for reuse.
- **Rich CLI Interface**: A visually appealing command-line interface built with the `rich` library, including progress bars and logs.
- **Supports Custom Data Types**: Extensible to handle custom parameter types or annotations.
- **Support for Tests on GitHub Repositories**: The GitHub package will be cloned locally, and a dependency graph will be generated using Topological Sorting and Depth-First Search (DFS) to analyze imports across various Python files. The execution flow will be determined based on this dependency graph.

---

## **How It Works**

### **Methods Overview**

#### **1. `generate_storage_data_structure(classes)`**
- **Purpose**: Creates a structured representation of the classes and their methods.
- **How It Works**:
  - Inspects methods of all classes.
  - Stores method signatures and parameter types.
  - Initializes an empty storage for instances and test data.
- **Output**: A dictionary mapping class names to their metadata.

#### **2. `randoop_test_generator(classes, sequence_number=2)`**
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

#### **3. `write_regression_tests(tot_sequences, module_name, file_path)`**
- **Purpose**: Writes the generated sequences as regression tests in `pytest` format.
- **How It Works**:
  - Iterates through successful sequences.
  - Generates Python test functions with proper assertions.
  - Saves the tests to a `regression_tests.py` file.
- **Output**: A reusable regression test file.

---

## **How to Run**

### **Requirements**

Ensure you have the following Python packages installed:

```bash
pip install rich tqdm pytest coverage
```

---

### **Installation and Usage with CLI**

This project provides a convenient command-line interface (CLI) for generating Randoop-style tests, simplifying the workflow.

---

### **Installation**

#### **1. Clone the Repository**
   ```bash
   git clone https://github.com/jay-karan/RandoopForPython.git
   cd RandoopForPython
   ```

#### **2. Install as a Python Package**
   ```bash
   pip install .
   ```

This will make the CLI tool available globally as `randoop-cli`.

---

### **Usage**

Once installed, you can use the CLI to generate Randoop-style tests with a simple command:

```bash
randoop-cli -f <path-to-python-file> -k <sequence-length>
```

- **`-f`**: Path to the Python file containing the class definitions.
- **`-k`**: (Optional) Number of test sequences to generate (default: `2`).

Please refer to the **Demo Section** of this Readme to run the default applications from the package.

#### **For GitHub Repositories**
You can use the following command to analyze a GitHub repository:

```bash
randoop-cli --repo-url <repo-url> -k <sequence-length>
```

We have created a simulated banking application GitHub repository for testing purposes, which you can find here: [BankApplication](https://github.com/soubhi/BankApplication). A demo is provided below.

#### **Multi-File Support**
You can also give multiple files by providing multiple `-f` parameters.

---

### **Output**

- **Test Results**:
  - Displays successful and error-prone sequences in the terminal.

- **Regression Tests**:
  - A `regression_tests.py` file is created in the working directory, containing reusable `pytest` test cases for the successful sequences.

---

## **Benefits of CLI Installation**

- **Global Access**: No need to navigate to the project directory every time—run the tool from anywhere.
- **Streamlined Workflow**: Simplified command structure for efficient testing.

With the CLI installed, integrating Randoop-style test generation into your development workflow becomes effortless! 🚀

---

## **Supported Functionality**

- **Dynamic Class Inspection**: Supports any Python class with methods.
- **Primitive Data Types**: Handles `int`, `float`, and `str` parameters.
- **Non-Primitive Data Types**: Handles the instances of other classes as parameters.

---

## **Project Structure**

```plaintext
.
├── data_generation.py          # Module for generating random primitive values.
├── coverage_analysis.py        # Module for analyzing test coverage.
├── test_generator.py           # Core logic for test generation and regression test writing.
├── cli.py                      # Command-line interface for running the tool.
├── module_loader.py            # Handles dynamic loading of classes.
├── regression_tests.py         # Automatically generated regression tests.
```

---

## **Demo of Randoop on Calculator Application - Primitive Types**

### **1. Clone the Repository**
```bash
git clone https://github.com/jay-karan/RandoopForPython.git
```

### **2. Navigate to the Project Directory**
```bash
cd RandoopForPython
```

### **3. Install the Tool**
```bash
pip install rich tqdm pytest coverage
pip install .
```

### **4. Run the Randoop-Style Test Generator**
```bash
randoop-cli -f CalculatorApplication.py -k 10
```

### **5. Observe the Output**
![Randoop CLI in Action for Calculator Application](assets/calculator_output.png)

![GitHub Application Demo](assets/calculator_demo.gif)

---

## **Demo of Randoop on Banking Application - Non-Primitive Type**

Repeat the same steps as above, replacing `CalculatorApplication.py` with `BankingApplication.py`. Below is an example of the output:
![Randoop CLI in Action for Banking Application](assets/banking_output.png)

![GitHub Application Demo](assets/banking_demo.gif)

---

## **Demo of Randoop on Employee Application - Non-Primitive Type**

Repeat the same steps as above, replacing `BankingApplication.py` with `EmployeeApplication.py`. Below is an example of the output:
![Randoop CLI in Action for Banking Application](assets/employee_output.png)

![GitHub Application Demo](assets/employee_demo.gif)

---

## **Demo of Randoop on Github Application - Non-Primitive Type**

Follow the command below to execute the tool for generating tests on a github project `https://github.com/soubhi/BankApplication`. The `--repo-url` flag specifies link for your application:

### **Run the Randoop-Style Test Generator**
```bash
randoop-cli --repo-url https://github.com/soubhi/BankApplication -k 10
```

![GitHub Application Demo](assets/github_demo.gif)

---

## **Contributing**

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

## **License**

This project is licensed under the MIT License.

---

## **Contact**

For questions or feedback, feel free to reach out by creating issues.

---
**Happy Coding! 🚀**
