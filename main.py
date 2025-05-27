import calculator
from view import View
import data_locations

#this class acts as the presenter in the MVP design pattern
class Presenter:
    def __init__(self):
        indices_info = data_locations.get_data_info()
        index_names = list(indices_info)
        profit_chances = calculator.get_profit_chances(index_names[0])
        self.ui = View(self, profit_chances, index_names)

    def get_chance_of_profit_list(self, index_name, minimum_profit_percentage_threshold, inflation):
        return calculator.get_profit_chances(index_name, minimum_profit_percentage_threshold, inflation)

presenter = Presenter()
