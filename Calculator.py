# This is sample example class
"""
class SampleClass:
    def add(self, a:int, b:int):
        return a + b

    def multiply(self, a:int, b:int):
        return a * b

class AnotherClass:
    def greet(self, name:str):
        return f"Hello, {name}!"

    def farewell(self):
        return "Goodbye!"
"""

# New Calculator class with various mathematical operations
class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        return base ** exponent

    def square_root(self, a: float) -> float:
        if a < 0:
            raise ValueError("Cannot calculate the square root of a negative number.")
        return a ** 0.5

"""
# New BankingApplication class with banking operations
class BankingApplication:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number: str, initial_balance: float = 0.0):
        if account_number in self.accounts:
            raise ValueError(f"Account {account_number} already exists.")
        self.accounts[account_number] = initial_balance
        return f"Account {account_number} created with balance {initial_balance}."

    def deposit(self, account_number: str, amount: float):
        if account_number not in self.accounts:
            raise ValueError(f"Account {account_number} does not exist.")
        self.accounts[account_number] += amount
        return f"Deposited {amount} to account {account_number}."

    def withdraw(self, account_number: str, amount: float):
        if account_number not in self.accounts:
            raise ValueError(f"Account {account_number} does not exist.")
        if self.accounts[account_number] < amount:
            raise ValueError(f"Insufficient funds in account {account_number}.")
        self.accounts[account_number] -= amount
        return f"Withdrew {amount} from account {account_number}."

    def get_balance(self, account_number: str) -> float:
        if account_number not in self.accounts:
            raise ValueError(f"Account {account_number} does not exist.")
        return self.accounts[account_number]
"""
