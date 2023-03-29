import pandas as pd
import numpy as np

# load csv as pandas dataframe
df = pd.read_csv('all_tickers_2020_2022.csv')
metadata = pd.read_csv('layoff_metadata.csv')
ticker_metadata = pd.read_csv('ticker_metadata1.csv')
ticker_metadata['ticker'] = ticker_metadata['ticker'].str.upper()

# change df date column to datetime
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')

df_transposed = df.set_index('date').transpose().reset_index()

# join meta data with ticker data to get ticker symbols
tickers_joined = pd.merge(metadata.set_index('company'), ticker_metadata.set_index('company name'), left_index=True, right_index=True).set_index('ticker').reset_index()

# join ticker metadata with stock data
stocks_data = pd.merge(tickers_joined['layoff_grouping'], df_transposed, left_index=True, right_index=True)

# group layoff vs no layoff groups
layoff_group = stocks_data[stocks_data['layoff_grouping']=='yes'].transpose().drop('layoff_grouping')
no_layoff_group = stocks_data[stocks_data['layoff_grouping']=='no'].transpose().drop('layoff_grouping')


def return_cumulative_return(portfolio_df):

    data = portfolio_df
    data.columns = data.iloc[0]

    # calculate percent change
    monthly_pct_change = data.drop('index').sort_index().pct_change()

    wts = np.empty(data.shape[1])
    wts.fill(1 / data.shape[1])
    weighted_return = (wts * monthly_pct_change)

    # portfolio calculation
    portfolio_return = weighted_return.sum(axis=1)
    cumprod_portfolio = (1 + portfolio_return).cumprod()

    return cumprod_portfolio

def create_return_dataframe():

    layoff_df = pd.DataFrame(return_cumulative_return(layoff_group), columns=['layoff_group'])
    no_layoff_df = pd.DataFrame(return_cumulative_return(no_layoff_group), columns=['no_layoff_group'])

    total_df = pd.merge(layoff_df, no_layoff_df, left_index=True, right_index=True)

    return total_df

create_return_dataframe().to_csv('cumulative_returns.csv', index=True)


