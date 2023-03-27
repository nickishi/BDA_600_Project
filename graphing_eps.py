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
from datetime import datetime, timedelta


def get_stock_price(ticker, date_range = None):
    """This function uses the ticker and date range
        to pull the daily stock prices before and after
        an earnings release. Final numbers returned is
        the percentage increase or decrease 2 days before
        and 2 days after the EPS release."""

    key = "4UGW7JB0G6QNPFPM"

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + ticker + '&apikey=' + key
    r = requests.get(url)
    data = r.json()
    #print(json.dumps(data, indent=4))
    ts_data = data["Time Series (Daily)"]
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2022, 12, 31)
    print(json.dumps(ts_data, indent = 4))

    #TODO: Use for loop to find two days before and two days after percentage change of EPS.
    for point in ts_data:
        if start_date <= datetime.strptime(point, '%Y-%m-%d') <= end_date:

            print(point)


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
            temp_list.append(point['reportedDate'])
            temp_list.append(point["surprisePercentage"])
            needed_data.append(temp_list)
            date_range.append(point['reportedDate'])
    print(needed_data)
    return needed_data, date_range

def main():

    #List of tickers
    ticker_list = ["AAPL", "MSFT", "NVDA", "UNH", "JNJ", "MRK", "RTX", "HON", "UPS", "BRK.B", "JPM", "BAC"]

    #TODO: Using for testing purposes. Delete after final for loop below is finished.
    get_stock_price("AAPL")

    #for ticker in ticker_list:

        #needed_data, date_range = get_eps(ticker)






if __name__ == "__main__":
    main()