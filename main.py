import calculator
from view import View
import data_locations

class Presenter:
    """This class acts as the presenter in the MVP design pattern"""

    def __init__(self):
        """Sets up the presenter by creating the UI and loading the initial data for the graph"""
        indices_info = data_locations.get_data_info()
        index_names = list(indices_info)
        profit_data = calculator.get_profit_chances(index_names[0])
        profit_chances = profit_data["profit_chances"]
        min_max_median_data = profit_data["min_max_median"]
        self.ui = View(self, profit_chances, min_max_median_data, index_names)

    def get_chance_of_profit_list(self, index_name, minimum_profit_percentage_threshold, inflation):
        """Presenter function which calls the calculator function"""
        return calculator.get_profit_chances(index_name, minimum_profit_percentage_threshold, inflation)

presenter = Presenter()
