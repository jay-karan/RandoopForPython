class Calculator:
    def __init__(self):
        """
        Initialize the Calculator with a default precision for results.
        :param precision: Number of decimal places for the output (default is 2).
        """
        self.precision = 2

    def format_result(self, result: float) -> float:
        """
        Format the result to the specified precision.
        :param result: The result of the operation.
        :return: The formatted result.
        """
        return round(result, self.precision)

    def add(self, a: float, b: float) -> float:
        return self.format_result(a + b)

    def subtract(self, a: float, b: float) -> float:
        return self.format_result(a - b)

    def multiply(self, a: float, b: float) -> float:
        return self.format_result(a * b)

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return self.format_result(a / b)

    def power(self, base: float, exponent: float) -> float:
        return self.format_result(base ** exponent)

    def square_root(self, a: float) -> float:
        if a < 0:
            raise ValueError("Cannot calculate the square root of a negative number.")
        return self.format_result(a ** 0.5)
