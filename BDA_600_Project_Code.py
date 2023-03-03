import requests
import json
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import math
from alpha_vantage.timeseries import TimeSeries
import time

def create_graphs(data, ticker):
    
    fig = plt.figure(dpi = 80, facecolor = "w", edgecolor = "k")
    data["5. adjusted close"].plot()
    plt.title("Stock Price of " + ticker + " from 2020 to end of 2022")
    plt.tight_layout()
    plt.grid()
    plt.show()

def create_save_graphs(data, ticker):
    fig = plt.figure(dpi = 80, facecolor = "w", edgecolor = "k")
    data["5. adjusted close"].plot()
    plt.title("Stock Price of " + ticker + " from 2020 to end of 2022")
    plt.tight_layout()
    plt.grid()
    plt.savefig(ticker + "_stock_price_2020_2022.png")
    print(ticker + " Graph saved")


def api_call(ticker_str = None, ticker_list = None):
    key = "4UGW7JB0G6QNPFPM"

    ts = TimeSeries(key, output_format = "pandas")

    if ticker_str != None:
        
           
        comp_data , comp_meta_data = ts.get_monthly_adjusted(symbol = ticker_str, outputsize='full')
  
        df2 = comp_data.loc["20200101" : "20221231"]
        create_graphs(df2, ticker)

            
            
                #print("1")
                #print("Invalid Ticker: " + company)


    elif ticker_str == None:
        for company in ticker_list:
            print(company)
            comp_data, comp_meta_data = ts.get_monthly_adjusted(symbol = company, outputsize = "full")
            df2 = comp_data.loc["20200101" : "20221231"]
            create_save_graphs(df2, company)
        
            #print("2")
            #print("Invalid Ticker: " + ticker)

    

    


def main():
    print("Hello World")
    exit = "yes"
    
    while exit == "yes":
        ticker = input("Enter a ticker: ")
        
        if ticker.upper() == "LIST":
            ###INSERT TICKERS INTO LIST AS STRINGS
            print("1")
            list_of_companies = ["AAPL", "XOM"]
            api_call(ticker_str = None, ticker_list = list_of_companies)
            
        else:
            print("2")
            api_call(ticker_str = ticker, ticker_list = None)
            
        #ticker_upper = ticker.upper()
        #data = api_call(ticker_upper)
        #create_graphs(data, ticker_upper)
        exit = input("Do you want to search another company (yes/no): ")












if __name__ == "__main__":
    
    main()
