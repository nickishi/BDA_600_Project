import requests
import json
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import math
from alpha_vantage.timeseries import TimeSeries

def create_graphs(data, ticker):
    
    
    data["5. adjusted close"].plot()
    plt.title("Stock Price of " + ticker + " from 2020 to end of 2022")
    plt.tight_layout()
    plt.grid()
    plt.show()




def api_call(ticker):
    key = "4UGW7JB0G6QNPFPM"

    ts = TimeSeries(key, output_format = "pandas")
    try:
        comp_data , comp_meta_data = ts.get_daily_adjusted(symbol = ticker, outputsize='full')
        print(comp_data)
        fig = plt.figure(dpi = 80, facecolor = "w", edgecolor = "k")
        print(comp_meta_data)
        df2 = comp_data.loc["20200101" : "20221231"]
        create_graphs(df2, ticker)
    except:
        print("Invalid Ticker: " + ticker)

    

    


def main():
    exit = "yes"
    while exit == "yes":
        ticker = input("Enter a ticker: ")
        ticker_upper = ticker.upper()
        data = api_call(ticker_upper)
        #create_graphs(data, ticker_upper)
        exit = input("Do you want to search another company (yes/no): ")












if __name__ == "__main__":
    main()
