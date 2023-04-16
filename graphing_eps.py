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
import numpy as np

def stock_price_calc_eps(ticker, eps_date_range, stock_date_range, stock_price_data, eps_data):

    before_eps = []
    after_eps = []
    for i in range(0, len(stock_date_range)):

        if stock_date_range[i] in eps_date_range:

            price_before_eps = round(((stock_price_data[i] - stock_price_data[i+1])/abs(stock_price_data[i+1]))*100, 3)
            before_eps.append(price_before_eps)
            #print(stock_date_range[i])
            #print("Stock Price Percent Change Before EPS: " + str(price_before_eps))
            price_after_eps = round(((stock_price_data[i-2] - stock_price_data[i-1])/abs(stock_price_data[i-1]))*100, 3)
            after_eps.append(price_after_eps)
            #print("Stock Price Percent Change after EPS: " + str(price_after_eps))
    print(eps_date_range)

    print(before_eps)
    print(after_eps)
    print(eps_data)

    if ticker != "BRK-B":

        eps_date_range.reverse()


        before_eps.reverse()
        after_eps.reverse()
        eps_data.reverse()

        eps_data = [float(value) for value in eps_data]
        n = len(eps_date_range)
        r = np.arange(n)
        width = 0.25
        plt.ylim(-5, 40)
        plt.title(ticker + " Stock Market Price Percentage Before and After EPS Percentage Release")
        plt.bar(r - width, before_eps, color='g',
                width=width, edgecolor='black',
                label='Stock Price Percent Change Before EPS')

        plt.bar(r, eps_data, color='b',
                width=width, edgecolor='black',
                label='EPS Percent On Earnings Release')

        plt.bar(r + width, after_eps, color='r',
                width=width, edgecolor='black',
                label='Stock Price Percent Change After EPS')

        plt.axhline(y=0, color='black', linestyle='-')
        plt.xticks(r + width/2, eps_date_range, rotation = 45)
        plt.xlabel("Date of Earnings Release")
        plt.ylabel("Percentage Change")
        plt.legend()
        plt.show()








def stock_price_eps_graph(ticker, eps_date_range, stock_date_range, stock_price_data, eps_data):
    """WTF do I want this to do?
        - Calculate percent change before and after EPS report date?
        - Do I want to graph the EPS date and stock price? Possibly different function
        - """

    fig, ax = plt.subplots()
    plt.plot(stock_date_range, stock_price_data)
    plt.title(ticker + " Stock Price and EPS Comparison 2020-2022")
    plt.xlabel("Date")
    plt.ylabel(ticker + " Closing Stock Price")
    stock_price_at_eps = []
    for i in range(0, len(stock_date_range)):

        if stock_date_range[i] in eps_date_range:

            stock_price_at_eps.append(stock_price_data[i])


    for stock_date, stock_price, eps_percent in zip(eps_date_range, stock_price_at_eps, eps_data):
        #plt.plot(stock_date, stock_price, marker = "o", markersize = 10, markerfacecolor="blue")
        ax.annotate(text = eps_percent + "%", xy=(stock_date, stock_price),
                    arrowprops=dict(facecolor='black', shrink=0.05))



        # plt.axvline(x = stock_date, color = 'b')

    plt.xticks(rotation=45)
    plt.savefig('EPS_Graphs/' + ticker + "_EPS_Stock_Price_Comparison_2020_2022.png", dpi = 1000)


def get_stock_price(ticker, date_range=None):
    """This function uses the ticker and date range
        to pull the daily stock prices before and after
        an earnings release. Final numbers returned is
        the percentage increase or decrease 2 days before
        and 2 days after the EPS release."""

    key = "4UGW7JB0G6QNPFPM"

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + ticker + '&outputsize=full' + '&apikey=' + key
    r = requests.get(url)
    data = r.json()
    # print(json.dumps(data, indent=4))
    ts_data = data["Time Series (Daily)"]
    start_date = date(2020, 1, 1)
    end_date = date(2022, 12, 31)

    needed_data_stock_price = []
    date_range = []

    # TODO: Use for loop to find two days before and two days after percentage change of EPS.
    for stock_date, value in ts_data.items():
        temp_list = []

        # print(stock_date)
        if start_date.strftime('%Y-%m-%d') <= stock_date <= end_date.strftime('%Y-%m-%d'):
            # temp_list.append(stock_date)
            needed_data_stock_price.append(float(value["5. adjusted close"]))
            date_range.append(datetime.strptime(stock_date, '%Y-%m-%d'))
            print(stock_date, value["5. adjusted close"])


    return needed_data_stock_price, date_range


def get_eps(ticker):
    """This function pulls the date and Earnings Per Share (EPS) percentage change
        for a given stock. Positive EPS generally indicates an increase in stock price
        and vice versa for negative EPS"""

    key = "4UGW7JB0G6QNPFPM"

    url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=' + ticker + '&apikey=' + key
    r = requests.get(url)
    data = r.json()

    print(json.dumps(data,  indent = 4))

    # Pulls just the quarterly earnings of a given ticker
    quart_data = data['quarterlyEarnings']

    # Needed data is formatted as 2-D list, inner lists are [Earnings report data, percentage differnce in reported and estimated EPS]
    needed_data = []
    date_range = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2022, 12, 30)

    #
    for point in quart_data:
        temp_list = []

        if start_date <= datetime.strptime(point['fiscalDateEnding'], '%Y-%m-%d') <= end_date:
            # temp_list.append(point['reportedDate'])
            needed_data.append(point["surprisePercentage"])
            # needed_data.append(temp_list)
            date_range.append(datetime.strptime(point['reportedDate'], '%Y-%m-%d'))
    print()
    print(date_range)
    # Needed data includes the date of the EPS and pecentage suprise. Format is 2-D list [[date, surpise EPS]]
    # date_range includes just the dates of the EPS release.
    return needed_data, date_range


def main():
    # List of tickers
    ticker_list = ["AAPL", "MSFT", "NVDA", "UNH", "JNJ", "MRK", "RTX", "HON", "UPS", "BRK-B", "JPM", "BAC"]

    # TODO: Using for testing purposes. Delete after final for loop below is finished.
    #stock_price_needed_data, stock_date_range = get_stock_price("MSFT")
    ##eps_needed_data, eps_date_range = get_eps("MSFT")
    #ticker = "MSFT"
    #stock_price_calc_eps(ticker, eps_date_range, stock_date_range, stock_price_needed_data, eps_needed_data)
    #stock_price_eps_graph(ticker, eps_date_range, stock_date_range, stock_price_needed_data, eps_needed_data)
    for ticker in ticker_list:

    #
        stock_price_needed_data, stock_date_range = get_stock_price(ticker)
    #
        eps_needed_data, eps_date_range = get_eps(ticker)
    #
        #stock_price_eps_graph(ticker, eps_date_range, stock_date_range, stock_price_needed_data, eps_needed_data)
        stock_price_calc_eps(ticker, eps_date_range, stock_date_range, stock_price_needed_data, eps_needed_data)


if __name__ == "__main__":
    main()
