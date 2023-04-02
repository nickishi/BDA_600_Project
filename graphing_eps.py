import requests
import json
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import math
from alpha_vantage.timeseries import TimeSeries
import time
import subprocess
import sys
import os.path
from datetime import datetime, timedelta, date

def stock_price_eps_graph(eps_date_range, stock_date_range, stock_price_data, eps_data):
    """WTF do I want this to do?
        - Calculate percent change before and after EPS report date?
        - Do I want to graph the EPS date and stock price? Possibly different function
        - """
    plt.plot(stock_date_range, stock_price_data)


    for date, eps in zip(eps_date_range, eps_data):
        plt.axvline(x = date, color = 'b')

    plt.xticks(rotation=45)

    plt.show()


def get_stock_price(ticker, date_range = None):
    """This function uses the ticker and date range
        to pull the daily stock prices before and after
        an earnings release. Final numbers returned is
        the percentage increase or decrease 2 days before
        and 2 days after the EPS release."""

    key = "4UGW7JB0G6QNPFPM"

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + ticker + '&outputsize=full' + '&apikey=' + key
    r = requests.get(url)
    data = r.json()
    #print(json.dumps(data, indent=4))
    ts_data = data["Time Series (Daily)"]
    start_date = date(2020, 1, 1)
    end_date = date(2022, 12, 31)

    needed_data_stock_price = []
    date_range = []

    #TODO: Use for loop to find two days before and two days after percentage change of EPS.
    for stock_date, value in ts_data.items():
        temp_list = []

        #print(stock_date)
        if start_date.strftime('%Y-%m-%d') <= stock_date <= end_date.strftime('%Y-%m-%d'):

            #temp_list.append(stock_date)
            needed_data_stock_price.append(float(value["5. adjusted close"]))
            date_range.append(datetime.strptime(stock_date, '%Y-%m-%d'))
            print(stock_date, value["5. adjusted close"])


    print(needed_data_stock_price)
    print(date_range)
    return needed_data_stock_price, date_range






def get_eps(ticker):
    """This function pulls the date and Earnings Per Share (EPS) percentage change
        for a given stock. Positive EPS generally indicates an increase in stock price
        and vice versa for negative EPS"""

    key = "4UGW7JB0G6QNPFPM"


    url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=' + ticker + '&apikey=' + key
    r = requests.get(url)
    data = r.json()

    print(json.dumps(data, indent = 4))

    #Pulls just the quarterly earnings of a given ticker
    quart_data = data['quarterlyEarnings']

    #Needed data is formatted as 2-D list, inner lists are [Earnings report data, percentage differnce in reported and estimated EPS]
    needed_data = []
    date_range = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2022, 12, 31)

    #
    for point in quart_data:
        temp_list = []

        if start_date <= datetime.strptime(point['fiscalDateEnding'], '%Y-%m-%d') <= end_date:
            #temp_list.append(point['reportedDate'])
            needed_data.append(point["surprisePercentage"])
            #needed_data.append(temp_list)
            date_range.append(datetime.strptime(point['reportedDate'], '%Y-%m-%d'))
    print(needed_data)
    print(date_range)

    #Needed data includes the date of the EPS and pecentage suprise. Format is 2-D list [[date, surpise EPS]]
    #date_range includes just the dates of the EPS release.
    return needed_data, date_range

def main():

    #List of tickers
    ticker_list = ["AAPL", "MSFT", "NVDA", "UNH", "JNJ", "MRK", "RTX", "HON", "UPS", "BRK.B", "JPM", "BAC"]

    #TODO: Using for testing purposes. Delete after final for loop below is finished.
    stock_price_needed_data, stock_date_range = get_stock_price("AAPL")
    eps_needed_data, eps_date_range = get_eps("AAPL")

    stock_price_eps_graph(eps_date_range, stock_date_range, stock_price_needed_data, eps_needed_data)
    #for ticker in ticker_list:

        #stock_price_needed_data, stock_date_range = get_stock_price(ticker)
        #eps_needed_data, eps_date_range = get_eps(ticker)









if __name__ == "__main__":
    main()