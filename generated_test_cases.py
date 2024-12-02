import pytest
from combined_test_cases import *

# Initialize instances
BankAccount_1 = BankAccount(NoneType(), -35.37119541518439)
SavingsAccount_1 = SavingsAccount(NoneType(), 43.30356124129503, 62.857035803393416)
CheckingAccount_1 = CheckingAccount(NoneType(), -94.84794010112519, 69.53356902432378)

# Test cases
def test_BankAccount_deposit_0():
    instance = BankAccount_1
    result = instance.deposit(18.719725676638603)
    assert result == -16.651469738545785

def test_BankAccount_get_balance_1():
    instance = BankAccount_1
    result = instance.get_balance()
    assert result == -16.651469738545785

def test_BankAccount_get_balance_2():
    instance = BankAccount_1
    result = instance.get_balance()
    assert result == -16.651469738545785

def test_BankAccount_get_balance_3():
    instance = BankAccount_1
    result = instance.get_balance()
    assert result == -16.651469738545785

def test_SavingsAccount_get_balance_4():
    instance = SavingsAccount_1
    result = instance.get_balance()
    assert result == 43.30356124129503

def test_SavingsAccount_get_balance_5():
    instance = SavingsAccount_1
    result = instance.get_balance()
    assert result == 43.30356124129503

def test_SavingsAccount_get_balance_6():
    instance = SavingsAccount_1
    result = instance.get_balance()
    assert result == 43.30356124129503

def test_SavingsAccount_add_interest_7():
    instance = SavingsAccount_1
    result = instance.add_interest()
    assert result == 2765.2370605998162

def test_SavingsAccount_withdraw_8():
    instance = SavingsAccount_1
    result = instance.withdraw(40.78795709119353)
    assert result == 2724.4491035086226

def test_SavingsAccount_add_interest_9():
    instance = SavingsAccount_1
    result = instance.add_interest()
    assert result == 173975.24394727318

def test_CheckingAccount_get_balance_10():
    instance = CheckingAccount_1
    result = instance.get_balance()
    assert result == -94.84794010112519

def test_CheckingAccount_deposit_11():
    instance = CheckingAccount_1
    result = instance.deposit(33.47854923578964)
    assert result == -61.369390865335546

def test_CheckingAccount_deposit_12():
    instance = CheckingAccount_1
    result = instance.deposit(84.76171682049423)
    assert result == 23.392325955158682

def test_CheckingAccount_withdraw_13():
    instance = CheckingAccount_1
    result = instance.withdraw(18.45315401186933)
    assert result == 4.939171943289352

def test_CheckingAccount_get_balance_14():
    instance = CheckingAccount_1
    result = instance.get_balance()
    assert result == 4.939171943289352

def test_CheckingAccount_deposit_15():
    instance = CheckingAccount_1
    result = instance.deposit(92.64505019531208)
    assert result == 97.58422213860143

def test_CheckingAccount_get_balance_16():
    instance = CheckingAccount_1
    result = instance.get_balance()
    assert result == 97.58422213860143

def test_CheckingAccount_get_balance_17():
    instance = CheckingAccount_1
    result = instance.get_balance()
    assert result == 97.58422213860143

def test_CheckingAccount_get_balance_18():
    instance = CheckingAccount_1
    result = instance.get_balance()
    assert result == 97.58422213860143

