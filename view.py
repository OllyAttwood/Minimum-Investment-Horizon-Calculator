import matplotlib.pyplot as plt

def setup_display(chance_of_profit_list):
    plt.plot(chance_of_profit_list)
    #plt.plot(smooth_line(chance_of_profit_list))
    plt.show()
