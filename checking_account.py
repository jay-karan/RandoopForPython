from bank_account import BankAccount

class CheckingAccount(BankAccount):
    """A CheckingAccount class that extends BankAccount with overdraft protection."""

    def __init__(self, account_holder: str, initial_balance: float = 0.0, overdraft_limit: float = 500.0):
        """
        Initialize the checking account with an overdraft limit.
        :param overdraft_limit: Maximum overdraft amount allowed (default is $500.0).
        """
        super().__init__(account_holder, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float):
        """
        Withdraw an amount from the account, considering overdraft protection.
        :param amount: The amount to withdraw.
        :raises ValueError: If withdrawal exceeds overdraft limit.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance + self.overdraft_limit:
            raise ValueError("Withdrawal exceeds overdraft limit.")
        self.balance -= amount
        return self.balance

    def __str__(self):
        """Return a string representation of the checking account."""
        return f"CheckingAccount({self.account_holder}, Balance: {self.balance}, Overdraft Limit: {self.overdraft_limit})"

