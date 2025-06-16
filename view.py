import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox
import matplotlib
from matplotlib.animation import FuncAnimation
from tkinter import messagebox, Tk
import numpy as np
import logging

class View:
    """The UI for the program"""

    def __init__(self, presenter, chance_of_profit_list, min_max_median_data, index_names):
        """Sets up the matplotlib UI"""
        self.presenter = presenter
        self.indices_checkbutton_options = index_names
        matplotlib.rcParams['toolbar'] = 'None' #removes matplotlib toolbar

        self.fig, self.ax = plt.subplots(num="Minimum Investment Horizon Calculator") #num is used as window title
        self.fig.set_figheight(7)
        self.fig.set_figwidth(9)
        self.fig.subplots_adjust(bottom=0.3, right=0.7) #increases bottom space

        self.index_colours = ["blue", "red", "yellow", "orange"]
        self.chart_lines = [[]] * len(index_names)
        for i in range(len(index_names)):
            line_data = [np.nan] * len(chance_of_profit_list) #initialise it with an empty line of the correct number of points
            if i == 0:
                line_data = chance_of_profit_list

            self.chart_lines[i] = plt.plot(line_data, color=self.index_colours[i])[0]
        plt.ylim(top=105, bottom=0) #top is 105 rather than 100 so the graph line is still visible at 100
        plt.xlim(left=0)
        x_tick_positions = [0,4,9,14,19,24,29]
        self.ax.set_xticks(ticks=x_tick_positions, labels=[tick+1 for tick in x_tick_positions])

        plt.title("Chance of Profit Over Time")
        plt.xlabel("Number of Years")
        plt.ylabel("Probability of Beating\nthe Minimum Profit Threshold (%)")

        indices_ax = plt.axes([0.71, 0.5, 0.27, 0.2])
        indices_ax.set_facecolor("grey")
        self.indices_checkbuttons = CheckButtons(indices_ax, self.indices_checkbutton_options, label_props={"color": self.index_colours})
        #modify the checkboxes appearance - https://stackoverflow.com/questions/42421363/customize-check-buttons-in-matplotlib
        self.indices_checkbuttons.set_active(0)
        self.indices_checkbuttons.on_clicked(lambda label: self.recalculate_graph()) #label parameter is not needed

        min_threshold_textbox_ax = plt.axes([0.3, 0.13, 0.4, 0.075])
        self.min_threshold_textbox = TextBox(min_threshold_textbox_ax, "Minimum profit threshold (%): ")
        self.min_threshold_textbox.set_val(str(0))
        self.min_threshold_textbox.on_submit(lambda text: self.chance_of_profit_settings_update(text, self.min_threshold_textbox))

        inflation_textbox_ax = plt.axes([0.3, .03, 0.4, 0.075])
        self.inflation_textbox = TextBox(inflation_textbox_ax, "Adjust for inflation of (%): ")
        self.inflation_textbox.set_val(0)
        self.inflation_textbox.on_submit(lambda text: self.chance_of_profit_settings_update(text, self.inflation_textbox))

        #setup cursor movement event handling for highlighting of graph column and min/max/median popup
        self.highlighted_column = None
        self.index_popup = None
        self.min_max_median_index_data = [[]] * len(index_names)
        self.min_max_median_index_data[0] = min_max_median_data
        self.fig.canvas.mpl_connect("motion_notify_event", self.mouse_move)

        plt.show()

    def chance_of_profit_settings_update(self, text, textbox):
        """This function is called whenever the settings are updated by the user, e.g. minimum profit threshold or inflation"""
        #try statement needed to catch the IndexError when the graph is hovered over where the  data doesn't cover i.e. the right-most column
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
        """Re-calculates the changes to the graph and updates it"""
        list_of_new_chance_of_profit_lists = []
        new_min_profit_threshold = float(self.min_threshold_textbox.text)
        new_inflation = float(self.inflation_textbox.text)

        for i, index_status in enumerate(self.indices_checkbuttons.get_status()):
            if index_status:
                index_name = self.indices_checkbutton_options[i]
                index_profit_data = self.presenter.get_chance_of_profit_list(index_name, new_min_profit_threshold, new_inflation)
                list_of_new_chance_of_profit_lists.append(index_profit_data["profit_chances"])
                self.min_max_median_index_data[i] = index_profit_data["min_max_median"]
            else:
                list_of_new_chance_of_profit_lists.append([])

        self.update_chart_lines(list_of_new_chance_of_profit_lists)

    def update_chart_lines(self, new_lines, num_overall_animation_frames=24):
        """Makes changes to the actual graph object from the given parameters"""
        self.animation_frames = []
        for i, new_line in enumerate(new_lines):
            self.animation_frames.append([])
            if new_line != []: #if index line should be updated (checkbox is ticked)
                orig_line = self.chart_lines[i].get_ydata()
                new_line = np.array(new_line)

                if np.isnan(orig_line).all(): #if the line isn't yet being displayed on the graph
                    for frame_num in range(num_overall_animation_frames):
                        self.animation_frames[i].append(new_line) #just adds the new line (each frame is the same as no animation is needed)
                else:
                    line_increase_per_frame = (new_line - orig_line) / num_overall_animation_frames
                    for frame_num in range(num_overall_animation_frames):
                        new_frame = orig_line + (line_increase_per_frame * (frame_num + 1))
                        self.animation_frames[i].append(new_frame)

        self.animation = FuncAnimation(self.fig, self.animate_chart, interval=20, frames=num_overall_animation_frames, repeat=False)
        self.fig.canvas.draw_idle() #forces the graph to redraw with the new data - otherwise it sometimes doesn't start animation until UI is interacted with further

    def animate_chart(self, i):
        """Specifies how the graph lines should be animated when changes are made"""
        for chart_line, new_line_data in zip(self.chart_lines, self.animation_frames):
            if new_line_data == []:
                chart_line.set_visible(False)
            else:
                chart_line.set_ydata(new_line_data[i])
                chart_line.set_visible(True)

    def mouse_move(self, event):
        """Handles mouse movement in the graph area. Specifically it controls the column highlighting and
        the min/max/median popups
        """
        x = event.xdata

        #remove previous highlighted column
        if self.highlighted_column != None:
            self.highlighted_column.remove()
            self.highlighted_column = None #needed otherwise error occurs when cursor leaves graph

        #add highlighted column in new position
        #also add min/max/median textbox if cursor is close enough
        if event.inaxes == self.ax: #if the cursor is within the graph area
            #highlight column
            x = round(x)
            self.highlighted_column = self.ax.axvspan(x-0.5, x+0.5, alpha=0.3)

            #add min/max/median popup if cursor is close enough
            y = event.ydata
            index_data_to_display = self.get_nearest_index(x, y)
            self.update_index_popup(index_data_to_display, event.xdata, y)

        self.fig.canvas.draw_idle() #forces the graph to redraw

    def get_nearest_index(self, x, y, min_distance=3):
        """Determines which index line on the chart is closest to the cursor (returns None if none are close enough)"""
        nearest_index = None
        nearest_distance = float("inf")

        #check each index graph lines to find which one is closest to the cursor (if any of them are close enough)
        try:
            for i, index_status in enumerate(self.indices_checkbuttons.get_status()):
                distance = abs(y - self.chart_lines[i].get_ydata()[x])

                if index_status and distance < min_distance and (nearest_index is None or distance < nearest_distance):
                    nearest_index = i
                    nearest_distance = distance
        except IndexError:
            logging.info("Handled the rightmost column being outside the data range (caught an IndexError produced by this)")

        return nearest_index

    def update_index_popup(self, index_num, x, y):
        """Update the popup which shows the min/max/median data for the nearest index line to the cursor"""
        if self.index_popup is not None:
            self.index_popup.set_visible(False)

        if index_num is not None:
            data_text = self.create_popup_text(self.min_max_median_index_data[index_num][round(x)], index_num, round(x)+1)
            box_style = {"color": self.index_colours[index_num], "alpha": 0.8}
            x += 1 #slightly adjust x so that cursor isn't too close to it

            #if cursor is near to right side, move the popup further left
            if x > 15:
                x -= 13

            self.index_popup = self.ax.text(x, y, data_text, bbox=box_style)

    def create_popup_text(self, min_max_median_dict, index_num, window_size):
        """Calculates what the text content of a popup should be"""
        index_name = self.indices_checkbutton_options[index_num]
        #r"$\bf{}$" is needed to make part of the text bold
        full_string = r"$\bf{" + index_name + " [" + str(window_size) + "-Year Periods]" + "}$"
        full_string += "\n——————————————"
        keys = ["min", "max", "median"]
        row_titles = ["Worst Period:   ", "Best Period:      ", "Median Period: "]

        for key, row_title in zip(keys, row_titles):
            change_percentage = (min_max_median_dict[key] - 1) * 100 #convert the figure to a percentage value
            change_percentage = round(change_percentage, 1) #round to one decimal place
            full_string += "\n" + r"$\bf{" + row_title + "}$" + str(change_percentage) + "%"

        #backslashes are needed in front of spaces otherwise the MathText formatting for the partial bold text removes the spaces
        full_string = full_string.replace(" ", "\ ")

        return full_string
