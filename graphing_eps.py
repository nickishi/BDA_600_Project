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


def get_eps(ticker):
    key = "4UGW7JB0G6QNPFPM"


    url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=' + ticker + '&apikey=' + key
    r = requests.get(url)
    data = r.json()

    print(json.dumps(data, indent = 4))

    quart_data = data['quarterlyEarnings']

    #Needed data is formatted as 2-D list, inner lists are [Earnings report data, percentage differnce in reported and estimated EPS]
    needed_data = []
    date_range = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2022, 12, 31)
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

    ticker_list = ["AAPL", "MSFT", "NVDA", "UNH", "JNJ", "MRK", "RTX", "HON", "UPS", "BRK.B", "JPM", "BAC"]

    get_eps(ticker_list[0])
    for ticker in ticker_list:

        pass






if __name__ == "__main__":
    main()