class BankingApplication:
    def create_account(self, account_number: str, initial_balance: float = 0.0):
        return account_number, initial_balance

    def deposit(self, account_number: str, current_balance: float, amount: float):
        new_balance = current_balance + amount
        return f"Deposited {amount} to account {account_number}. New balance: {new_balance}", new_balance

    def withdraw(self, account_number: str, current_balance: float, amount: float):
        if current_balance < amount:
            raise ValueError(f"Insufficient funds in account {account_number}.")
        new_balance = current_balance - amount
        return f"Withdrew {amount} from account {account_number}. Remaining balance: {new_balance}", new_balance

    def get_balance(self, account_number: str, current_balance: float) -> float:
        return current_balance
