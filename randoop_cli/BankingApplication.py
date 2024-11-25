class BankAccount:
    """A simple BankAccount class."""

    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        """Initialize the account with the account holder's name and initial balance."""
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount: float):
        """Deposit an amount into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float):
        """Withdraw an amount from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        """Return the current balance of the account."""
        return self.balance

    def __str__(self):
        """Return a string representation of the account."""
        return f"BankAccount({self.account_holder}, Balance: {self.balance})"
