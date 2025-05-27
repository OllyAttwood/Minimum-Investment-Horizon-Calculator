import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox
import matplotlib
from tkinter import messagebox, Tk
import numpy as np

class View:
    def __init__(self, presenter, chance_of_profit_list, index_names):
        self.presenter = presenter
        self.indices_checkbutton_options = index_names
        matplotlib.rcParams['toolbar'] = 'None' #removes matplotlib toolbar

        self.fig, self.ax = plt.subplots()
        self.fig.set_figheight(6)
        self.fig.subplots_adjust(bottom=0.3) #increases bottom space

        self.chart_lines = [[]] * len(index_names)
        for i in range(len(index_names)):
            line_data = [np.nan] * len(chance_of_profit_list) #initialise it with an empty line of the correct number of points
            if i == 0:
                line_data = chance_of_profit_list

            self.chart_lines[i] = plt.plot(line_data)[0]
        plt.ylim(top=105, bottom=0) #top is 105 rather than 100 so the graph line is still visible at 100
        plt.xlim(left=0)
        x_tick_positions = [0,4,9,14,19,24,29]
        self.ax.set_xticks(ticks=x_tick_positions, labels=[tick+1 for tick in x_tick_positions])

        indices_ax = plt.axes([0.5, 0.31, 0.39, 0.2])
        indices_ax.set_facecolor("#90D5FF")
        self.indices_checkbuttons = CheckButtons(indices_ax, self.indices_checkbutton_options)
        #modify the checkboxes appearance - https://stackoverflow.com/questions/42421363/customize-check-buttons-in-matplotlib
        self.indices_checkbuttons.set_active(0)
        self.indices_checkbuttons.on_clicked(lambda label: self.recalculate_graph()) #label parameter is not needed

        min_threshold_textbox_ax = plt.axes([0.5, 0.15, 0.4, 0.075])
        self.min_threshold_textbox = TextBox(min_threshold_textbox_ax, "Minimum profit threshold (%): ")
        self.min_threshold_textbox.set_val(str(0))
        self.min_threshold_textbox.on_submit(lambda text: self.chance_of_profit_settings_update(text, self.min_threshold_textbox))

        inflation_textbox_ax = plt.axes([0.5, .05, 0.4, 0.075])
        self.inflation_textbox = TextBox(inflation_textbox_ax, "Adjust for inflation of (%): ")
        self.inflation_textbox.set_val(0)
        self.inflation_textbox.on_submit(lambda text: self.chance_of_profit_settings_update(text, self.inflation_textbox))

        plt.show()

    def chance_of_profit_settings_update(self, text, textbox):
        try:
            #remove leading zero from textbox if there is one
            if len(text) > 1 and text[0] == "0":
                textbox.set_val(text[1:])

            #update graph
            self.recalculate_graph()

        except ValueError:
            root = Tk()
            root.withdraw() #the root has to be created and withrawn otherwise a blank window will appear in the background
            messagebox.showerror("Input Error", "Only numbers are allowed!")

    def recalculate_graph(self):
        list_of_new_chance_of_profit_lists = []
        new_min_profit_threshold = float(self.min_threshold_textbox.text)
        new_inflation = float(self.inflation_textbox.text)

        for i, index_status in enumerate(self.indices_checkbuttons.get_status()):
            if index_status:
                index_name = self.indices_checkbutton_options[i]
                list_of_new_chance_of_profit_lists.append(self.presenter.get_chance_of_profit_list(index_name, new_min_profit_threshold, new_inflation))
            else:
                list_of_new_chance_of_profit_lists.append([])

        self.update_chart_lines(list_of_new_chance_of_profit_lists)

    def update_chart_lines(self, new_lines):
        for i, new_line in enumerate(new_lines):
            if new_line == []:
                self.chart_lines[i].set_visible(False)
            else:
                self.chart_lines[i].set_ydata(new_line)
                self.chart_lines[i].set_visible(True)

        self.fig.canvas.draw_idle() #forces the graph to redraw with the new data
