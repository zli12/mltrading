"""Utility functions"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        # TODO: Read and join data for each symbol
        path = symbol_to_path(symbol)
        df_temp = pd.read_csv(path,index_col='Date',parse_dates=True,usecols=['Date','Adj Close'],na_values=['nan'])
        df_temp = df_temp.rename(columns = {'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':
        	df = df.dropna(subset=["SPY"])

    return df

def get_rolling_mean(values, window):
    return values.rolling(window=window,center=False).mean()

def get_rolling_std(values, window):
    return values.rolling(window=window,center=False).std()

def get_bollinger_bands(rm, rstd):
    upper_band = rm + 2*rstd
    lower_band = rm - 2*rstd
    return upper_band, lower_band

def test_run():
    # Define a date range
    start_date = '2016-01-05'
    end_date = '2017-01-05'
    dates = pd.date_range(start_date,end_date)

    # Choose stock symbols to read
    symbols = ['SPY', 'GOOG', 'IBM', 'AAPL']
    
    # Get stock data
    df = get_data(symbols, dates)

    rm_SPY = get_rolling_mean(df['SPY'],window=20)
    rstd_SPY = get_rolling_std(df['SPY'],window=20)
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)

    ax = df['SPY'].plot(title="Bollinger Bands", label='SPY')
    rm_SPY.plot(label='Rolling mean',ax=ax)
    upper_band.plot(label='upper band',ax=ax)
    lower_band.plot(label='lower band',ax=ax)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()
    #plot_data(normalize_date(df))   

    # compute global statistics
    #print df.mean()
    #print df.std()

def plot_data(df,title="Stock prices"):
    '''Plot stock prices'''
    ax = df.plot(title = title,fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def normalize_date(df):
    return df/ df.ix[0] * 100

if __name__ == "__main__":
    test_run()
