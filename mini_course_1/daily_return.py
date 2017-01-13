"""Utility functions"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

def symbol_to_path(symbol, base_dir="../data"):
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

def compute_daily_return(df):
    dfs = df.shift(1);
    dfs.ix[0,:] = dfs.ix[1,:]
    print dfs
    return 100*(df / dfs - 1)

def test_run():
    # Define a date range
    start_date = '2016-11-05'
    end_date = '2017-01-05'
    dates = pd.date_range(start_date,end_date)

    # Choose stock symbols to read
    symbols = ['SPY', 'GOOG']
    
    # Get stock data
    df = get_data(symbols, dates)
    plot_data(normalize_date(df))
    
    daily_return = compute_daily_return(df)
    print daily_return
    plot_data(daily_return, title="Daily returns",ylabel="Daily returns")

def plot_data(df,title="Stock prices",xlabel='Date',ylabel='Price'):
    '''Plot stock prices'''
    ax = df.plot(title = title,fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def normalize_date(df):
    return df/ df.ix[0] * 100

if __name__ == "__main__":
    test_run()
