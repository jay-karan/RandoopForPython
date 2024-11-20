import pytest
from sample import *

def test_Calculator_divide_0():
    instance = Calculator()
    result = instance.divide(14.153683183819737, 70.54741751938431)
    assert result == 0.20062652442140394

def test_Calculator_power_0():
    instance = Calculator()
    result = instance.power(-97.94551208263648, 60.88906063199079)
    assert isinstance(result, complex)

def test_Calculator_power_0():
    instance = Calculator()
    result = instance.power(-97.94551208263648, 60.88906063199079)
    assert isinstance(result, complex)

def test_Calculator_add_1():
    instance = Calculator()
    result = instance.add(-96.91809975766535, 36.1899882456176)
    assert result == -60.72811151204775

