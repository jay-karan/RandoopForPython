class Person:
    def __init__(self, name: str, age: int):
        """
        Initialize a Person instance.
        :param name: Name of the person.
        :param age: Age of the person.
        """
        self.name = name
        self.age = age

    def __str__(self):
        """Return a human-readable string representation of the person."""
        return f"{self.name}, Age: {self.age}"


class Company:
    def __init__(self, name: str):
        """
        Initialize a Company instance.
        :param name: Name of the company.
        """
        self.name = name
        self.employees = []  # Dependency on Person class

    def add_employee(self, person: Person):
        """
        Add an employee to the company.
        :param person: A Person instance representing the employee.
        """
        self.employees.append(person)

    def get_employees(self):
        """
        Get a list of all employees in the company.
        :return: List of Person instances.
        """
        return self.employees

    def __str__(self):
        """Return a human-readable string representation of the company."""
        return f"Company: {self.name}, Employees: {[str(e) for e in self.employees]}"
