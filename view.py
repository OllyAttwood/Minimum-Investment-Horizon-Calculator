import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, TextBox
import matplotlib
from tkinter import messagebox, Tk

class View:
    def __init__(self, presenter, chance_of_profit_list):
        self.presenter = presenter
        self.radio_button_options = ("Real Values", "Smoothed Values")
        matplotlib.rcParams['toolbar'] = 'None' #removes matplotlib toolbar

        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(bottom=0.2) #increases bottom space

        self.chart = plt.plot(chance_of_profit_list)[0]
        plt.ylim(top=105, bottom=0) #top is 105 rather than 100 so the graph line is still visible at 100
        plt.xlim(left=0)

        radio_ax = plt.axes([0.59, 0.21, 0.3, 0.2])
        radio_ax.set_facecolor("#90D5FF")
        radio_buttons = RadioButtons(radio_ax, self.radio_button_options, active=0, activecolor="orange")
        radio_buttons.on_clicked(self.index_radio_click)

        min_threshold_textbox_ax = plt.axes([0.5, 0.05, 0.4, 0.075])
        min_threshold_textbox = TextBox(min_threshold_textbox_ax, "Minimum profit threshold (%): ")
        min_threshold_textbox.set_val("0")
        min_threshold_textbox.on_submit(self.min_threshold_update)

        plt.show()

    def index_radio_click(label):
        pass

    def min_threshold_update(self, text):
        try:
            new_chance_of_profit_list = self.presenter.get_chance_of_profit_list(float(text))
            self.chart.set_ydata(new_chance_of_profit_list)
            self.fig.canvas.draw_idle() #forces the graph to redraw with the new data
        except ValueError:
            root = Tk()
            root.withdraw() #the root has to be created and withrawn otherwise a blank window will appear in the background
            messagebox.showerror("Input Error", "Only numbers are allowed!")
