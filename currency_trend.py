import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime

from load_currency_data import neg_beta_currencies

lookback = 50

# neg_beta_currencies = neg_beta_currencies['2019':]
neg_beta_currencies_ma = neg_beta_currencies.rolling(lookback).mean()

# remove nan
neg_beta_currencies_ma.dropna(axis=0, inplace=True)

# define date we want to move forward from
first_date = neg_beta_currencies_ma.index[0]

# adjust data to exclude dates before the moving average is calculated
neg_beta_currencies = neg_beta_currencies[first_date:]

index_dates = neg_beta_currencies.index
securities = neg_beta_currencies.columns

# creating new dataframe to create index of dates where currencies are in uptrend
positions = pd.DataFrame(columns=securities, index=index_dates, data=None)

# go through each currency and determine whether they're trading above below moving average, period of ma is "lookback"
for security in securities:

    # setting the value of long positions to 1. When the stock price > ma
    positions.loc[neg_beta_currencies[security].shift(1) > neg_beta_currencies_ma[security], security] = 1

# setting the value of short/no position to 0
positions.fillna(0, inplace=True)









