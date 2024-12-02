import pytest
from combined_test_cases import *

# Initialize instances
Person_1 = Person('woARN', -85)
Company_1 = Company('dDveR')

# Test cases
def test_Company_add_employee_0():
    instance = Company_1
    result = instance.add_employee(Person())
    assert isinstance(result, NoneType)

def test_Company_add_employee_1():
    instance = Company_1
    result = instance.add_employee(Person())
    assert isinstance(result, NoneType)

