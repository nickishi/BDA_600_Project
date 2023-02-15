import requests
import json
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import math
from alpha_vantage.timeseries import TimeSeries

def create_graphs(data, ticker):
    
    
    df2["4. adjusted close"].plot()
    plt.title("Stock Price of " + ticker + " from 2020 to end of 2022")
    plt.tight_layout()
    plt.grid()
    plt.show()




def api_call(ticker):
    key = "4UGW7JB0G6QNPFPM"

    ts = TimeSeries(key, output_format = "pandas")
    
    comp_data , comp_meta_data = ts.get_daily_adjusted(symbol = ticker, outputsize='full')
    print(comp_data)
    fig = plt.figure(dpi = 80, facecolor = "w", edgecolor = "k")
    print(comp_meta_data)
    df2 = comp_data.loc["20200101" : "20221231"]
    create_graphs(df2, ticker)
    

    


def main():
    exit = "no"
    while exit == "no":
        ticker = input("Enter a ticker: ")
        ticker_upper = ticker.upper()
        data = api_call(ticker_upper)
        create_graphs(data, ticker_upper)













if __name__ == "__main__":
    main()
