class Bill:
    """
    Object that contains data about a bill, such as
    total amount and period of the bill.
    """

    def __init__(self, amount: float, period: int):
        self.amount = amount
        self.period = period

    def printBills( amount: float, period: int):
        return f"Account {amount} for {period} days."


class Flatmate:
    """
    Creates a flatmate person who lives in the flat
    and pays a share of the bill.
    """

    def __init__(self, name: str, days_in_house: int):
        self.name = name
        self.days_in_house = days_in_house


    def pays(self, bill: float, flatmate2: str):
        weight = self.days_in_house / (self.days_in_house + flatmate2.days_in_house)
        to_pay = bill.amount * weight
        return to_pay
