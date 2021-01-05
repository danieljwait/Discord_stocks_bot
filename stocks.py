#!/usr/bin/env python

import pickle
import random


# Exits code when necessary modules are missing
def missing_package() -> None:
    print("Some modules required to run this program are missing\n"
          "Run setup.cmd and try again\n\n"
          "Press any key to continue . . . ", end="")
    input()
    exit()


try:
    import matplotlib.pyplot as plt
except ImportError:
    missing_package()

STOCKS_LIST = ["League of Legends", "Rust", "Hearthstone"]
DEFAULT_VALUE = 0.5
BUY_SELL_MARGIN = 0.02
FIXED_DP = 4  # Decimal points of accuracy


# Path to the data files
def data_path(stock_name: str) -> str:
    return "Data/" + stock_name + ".data"


# Path to the graph images
def graph_path(stock_name: str) -> str:
    return "Graphs/" + stock_name


# Saves stock data (in .data file)
def save_data(data: list, stock_name: str) -> None:
    with open(data_path(stock_name), 'wb+') as file:  # Overwrites any existing file
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)


# Loads the previous data on the stock
def load_stock_history(stock_name: str) -> list:
    try:  # Fetches past stock data
        with open(data_path(stock_name), 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:  # Creates start point if one doesnt exist
        return [DEFAULT_VALUE]


# Adds changes into the next value of the stock
def gen_next_value(value: float, data: list) -> float:
    if value >= 0.05:
        new_value = value * random.uniform(0.9, 1.1)
    else:  # When nearly a turning point
        new_value = value + random.choice([-0.01, 0, 0.01])  # Decrease, hold, increase
        if new_value < 0:  # Stops negative cost values
            new_value = abs(new_value)

    data.insert(0, new_value)
    return new_value


# Plots the graph and saves to a .png
def plot(stock_data: list, stock_name: str, days_shown: int) -> None:
    # Gets the last 50 day's worth of stocks
    plotting_data = stock_data[:days_shown + 1]

    # Plots buy line
    plt.plot(plotting_data, color="red", label="£"+format(plotting_data[0], '.' + str(FIXED_DP) + 'f'))

    # Changes data to plot the sell line
    for data in range(len(plotting_data)):
        plotting_data[data] += BUY_SELL_MARGIN

    # Plots sell line
    plt.plot(plotting_data, color="green", label="£"+format(plotting_data[0], '.' + str(FIXED_DP) + 'f'))

    # Draws the rest of the graph
    plt.ylabel("Price per stock (£)")
    plt.xlabel("Days ago")
    plt.axis([days_shown, 0, 0, 1.5])
    plt.title(stock_name)
    plt.legend()
    plt.savefig(graph_path(stock_name))
    plt.clf()  # Clears figure to allow next graph to be drawn


# Adds the necessary data to a table
def add_to_table(table: list, data: list) -> None:
    table[1].append(format(data[0] + BUY_SELL_MARGIN, '.' + str(FIXED_DP) + 'f'))  # Buy price
    table[2].append(format(data[0], '.' + str(FIXED_DP) + 'f'))  # Sell price
    table[3].append(str(len(data) - 1))  # Days open


# Uses unicode characters to 'draw' a table of info
def summary_table_string(data: list, headers: list) -> str:
    column_widths = []

    # Iterates through both data and headers and compares the max width of each, largest is used
    for column, header_width in zip(data, list(map(len, headers))):
        data_max_width = len(max(column, key=len))
        column_widths.append(data_max_width) if data_max_width > header_width else column_widths.append(header_width)

    # Top of table
    table_str = "┌─"
    for width in column_widths:
        table_str += ("─" * width) + "─┬─"
    table_str = table_str[:-2] + "┐\n"

    # Header row
    table_str += "| "
    for column, width in zip(headers, column_widths):
        table_str += f"{column:^{width}} | "
    table_str = table_str[:-1] + "\n"

    # Header to data divider
    table_str += "├─"
    for width in column_widths:
        table_str += ("─" * width) + "─┼─"
    table_str = table_str[:-2] + "┤\n"

    # Data rows
    for row in range(len(data[0])):
        table_str += "| "
        for column in range(len(data)):
            table_str += f"{data[column][row]:<{column_widths[column]}} | "
        table_str = table_str[:-1] + "\n"

    # Bottom of table
    table_str += "└─"
    for width in column_widths:
        table_str += ("─" * width) + "─┴─"
    table_str = table_str[:-2] + "┘"

    return table_str


# Does one update to all the stocks (1 day)
def update_stocks() -> None:
    for stock in STOCKS_LIST:
        stock_data = load_stock_history(stock)  # Loads data
        gen_next_value(stock_data[0], stock_data)  # Generates next value
        save_data(stock_data, stock)  # Saves data


# Creates a summary table of the day
def summary_table() -> str:
    table_headers = ["Stock", "Buy(£)", "Sell(£)", "Days open"]
    table_data = [STOCKS_LIST, [], [], []]

    for stock in STOCKS_LIST:
        stock_data = load_stock_history(stock)
        add_to_table(table_data, stock_data)

    return summary_table_string(table_data, table_headers)


# Creates plots of the latest data
def update_plots(days: int) -> None:
    for stock_name in STOCKS_LIST:
        stock_data = load_stock_history(stock_name)
        plot(stock_data, stock_name, days)


# Runs when the script is not imported
if __name__ == '__main__':
    update_stocks()
    update_plots(50)  # Default plot is last 50 days

    #  Uncomment for summary table
    #  print(summary_table())
