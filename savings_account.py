from bank_account import BankAccount

class SavingsAccount(BankAccount):
    """A SavingsAccount class that extends BankAccount with interest calculation."""

    def __init__(self, account_holder: str, initial_balance: float = 0.0, interest_rate: float = 0.02):
        """
        Initialize the savings account with an interest rate.
        :param interest_rate: Annual interest rate as a decimal (default is 0.02 for 2%).
        """
        super().__init__(account_holder, initial_balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        """Add interest to the current balance."""
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        return self.balance

    def __str__(self):
        """Return a string representation of the savings account."""
        return f"SavingsAccount({self.account_holder}, Balance: {self.balance}, Interest Rate: {self.interest_rate})"

