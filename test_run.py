"""Utility functions"""

import os
import pandas as pd
import matplotlib.pyplot as plt

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


def test_run():
    # Define a date range
    start_date = '2016-01-22'
    end_date = '2016-11-26'
    dates = pd.date_range(start_date,end_date)

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'AAPL']
    
    # Get stock data
    df = get_data(symbols, dates)
    q_start_date = '2016-01-01'
    q_end_date = '2016-07-31'
    #df1 = df[q_start_date:q_end_date,['AAPL','IBM']]
    df1 = df.ix[q_start_date:q_end_date,['AAPL','IBM']]
    #df1 = df1/df1[0]
    plot_data(normalize_date(df1))   

def plot_data(df,title="Stock prices"):
    '''Plot stock prices'''
    ax = df.plot(title = title,fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def normalize_date(df):
    return df/ df.ix[0,:]

if __name__ == "__main__":
    test_run()
