# this class acts as the presenter class in the MVP pattern
import calculator
import view

profit_chances = calculator.get_profit_chances()
view.setup_display(profit_chances)
