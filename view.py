import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox
import matplotlib
from tkinter import messagebox, Tk

class View:
    def __init__(self, presenter, chance_of_profit_list):
        self.presenter = presenter
        self.indices_checkbutton_options = ("S&P 500", "Index2", "Index3", "Index4")
        matplotlib.rcParams['toolbar'] = 'None' #removes matplotlib toolbar

        self.fig, self.ax = plt.subplots()
        self.fig.set_figheight(6)
        self.fig.subplots_adjust(bottom=0.3) #increases bottom space

        self.chart = plt.plot(chance_of_profit_list)[0]
        plt.ylim(top=105, bottom=0) #top is 105 rather than 100 so the graph line is still visible at 100
        plt.xlim(left=0)

        indices_ax = plt.axes([0.59, 0.31, 0.3, 0.2])
        indices_ax.set_facecolor("#90D5FF")
        indices_checkbuttons = CheckButtons(indices_ax, self.indices_checkbutton_options)
        #modify the checkboxes appearance - https://stackoverflow.com/questions/42421363/customize-check-buttons-in-matplotlib
        indices_checkbuttons.set_active(0)
        indices_checkbuttons.on_clicked(self.indices_checkbutton_click)

        min_threshold_textbox_ax = plt.axes([0.5, 0.15, 0.4, 0.075])
        self.min_threshold_textbox = TextBox(min_threshold_textbox_ax, "Minimum profit threshold (%): ")
        self.min_threshold_textbox.set_val(str(0))
        self.min_threshold_textbox.on_submit(lambda text: self.chance_of_profit_settings_update(text, self.min_threshold_textbox))

        inflation_textbox_ax = plt.axes([0.5, .05, 0.4, 0.075])
        self.inflation_textbox = TextBox(inflation_textbox_ax, "Adjust for inflation of (%): ")
        self.inflation_textbox.set_val(0)
        self.inflation_textbox.on_submit(lambda text: self.chance_of_profit_settings_update(text, self.inflation_textbox))

        plt.show()

    def indices_checkbutton_click(self, label):
        pass

    def chance_of_profit_settings_update(self, text, textbox):
        try:
            #remove leading zero if there is one
            if len(text) > 1 and text[0] == "0":
                textbox.set_val(text[1:])

            #update graph
            new_min_profit_threshold = float(self.min_threshold_textbox.text)
            new_inflation = float(self.inflation_textbox.text)
            new_chance_of_profit_list = self.presenter.get_chance_of_profit_list(new_min_profit_threshold, new_inflation)
            self.chart.set_ydata(new_chance_of_profit_list)
            self.fig.canvas.draw_idle() #forces the graph to redraw with the new data

        except ValueError:
            root = Tk()
            root.withdraw() #the root has to be created and withrawn otherwise a blank window will appear in the background
            messagebox.showerror("Input Error", "Only numbers are allowed!")
