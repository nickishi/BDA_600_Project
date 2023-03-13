import pandas as pd

# load csv as pandas dataframe
df = pd.read_csv('all_tickers_2020_2022.csv')
metadata = pd.read_csv('layoff_metadata.csv')
ticker_metadata = pd.read_csv('ticker_metadata1.csv')
ticker_metadata['ticker'] = ticker_metadata['ticker'].str.upper()

df_transposed = df.transpose()

# join meta data with ticker data to get ticker symbols
tickers_joined = pd.merge(metadata.set_index('company'), ticker_metadata.set_index('company name'), left_index=True, right_index=True).set_index('ticker')
print(tickers_joined)
