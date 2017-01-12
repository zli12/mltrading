import numpy as numpy
import pandas as pd 
from pandas_datareader import data as web
import seaborn as sns;sns.set()
import matplotlib.pyplot as plt

symbols = ['IBM','GOOG','SPY','BBY','T','MSFT']

for symbol in symbols:
	df = web.DataReader(symbol, data_source='yahoo')
	df.to_csv("data/{}.csv".format(symbol))

#AAPL = web.DataReader('AAPL', data_source='yahoo')
#type(AAPL)
#AAPL.info()
#AAPL.to_csv('data/AAPL.csv')
#print AAPL.tail()
#AAPL['Adj Close'].plot(figsize=(10,6))
#plt.show()