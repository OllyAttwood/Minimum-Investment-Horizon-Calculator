#this class acts as the presenter in the MVP design pattern
import calculator
from view import View

class Presenter:
    def __init__(self):
        profit_chances = calculator.get_profit_chances()
        self.ui = View(self, profit_chances)

    def get_chance_of_profit_list(self, minimum_profit_percentage_threshold, inflation):
        return calculator.get_profit_chances(minimum_profit_percentage_threshold, inflation)

presenter = Presenter()
