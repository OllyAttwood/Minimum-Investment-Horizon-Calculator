#this class acts as the presenter in the MVP design pattern
import calculator
from view import View
import data_locations

class Presenter:
    def __init__(self):
        indices_info = data_locations.get_data_info()
        index_names = [index_info["name"] for index_info in indices_info]
        profit_chances = calculator.get_profit_chances()
        self.ui = View(self, profit_chances, index_names)

    def get_chance_of_profit_list(self, minimum_profit_percentage_threshold, inflation):
        return calculator.get_profit_chances(minimum_profit_percentage_threshold, inflation)

presenter = Presenter()
