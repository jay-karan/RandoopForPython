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

## **Limitations**

#### **1. Limited Support for Complex Data Types**
- **Current Scope**: The tool effectively handles primitive and non-primitive data types like integers, floats, strings, and other classes.
- **Limitation**: It struggles with more complex data types such as images, videos, or other unstructured data as method arguments.
- **Impact**: Methods requiring these data types cannot be tested comprehensively.

#### **2. Challenges with Stateful Methods**
- **Current Scope**: The tool can invoke methods in sequence but does not track or adapt to state changes effectively.
- **Limitation**: Methods that depend on an object's internal state may produce invalid results or exceptions if called out of sequence.
- **Impact**: Tests may fail due to incorrect assumptions about method invocation order, rather than actual code errors.

#### **3. Handling of Exceptions**
- **Current Scope**: The tool logs exceptions encountered during test generation.
- **Limitation**: Limited analysis of exceptions is performed. Exceptions are logged but not categorized or analyzed for patterns.
- **Impact**: Developers must manually review exceptions to understand their causes and significance.

#### **4. Redundancy in Generated Tests**
- **Current Scope**: Test generation relies on randomness, often leading to repetitive or redundant tests.
- **Limitation**: Many generated test cases are duplicates or test the same functionality with slight variations in inputs.
- **Impact**: Results in unnecessary bloating of the regression test file, making it harder to review or maintain.

#### **5. No Test Case Prioritization**
- **Current Scope**: The tool generates test cases sequentially without considering test priority or impact.
- **Limitation**: High-priority methods or critical paths are not given precedence over less impactful ones.
- **Impact**: Test coverage may not align with the actual importance of features or code segments.

#### **6. Limited Scalability**
- **Current Scope**: Suitable for small to medium-sized projects.
- **Limitation**: Performance may degrade when handling large or complex codebases with multiple interdependent classes.
- **Impact**: Generates incomplete or suboptimal test cases for large projects.

#### **7. Lack of Sequence Persistence**
- **Current Scope**: The tool successfully generates sequences, reuses non-primitive data types, and employs feedback mechanisms to enhance test generation.
- **Limitation**: It currently does not support writing the generated sequences to a file for reuse or further analysis.
- **Impact**: Generated sequences are lost after execution, preventing long-term utilization or manual review of test cases.

---

## **Future Work and Improvements**

To address these limitations, the following enhancements are proposed:
1. Implement advanced data generation strategies for complex and nested data types.
2. Add edge case generation algorithms to complement random input generation.
3. Develop a state-aware testing mechanism for state-dependent methods.
4. Enhance exception handling by categorizing and analyzing exceptions.

---

## **License**

This project is licensed under the MIT License.

---

## **Contact**

For questions or feedback, feel free to reach out by creating issues.

---
**Happy Coding! 🚀**
