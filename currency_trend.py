import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime

from load_currency_data import neg_beta_currencies, neg_beta_currencies_pct
from market_risk import risk_on

lookback = 200

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

# adding the "risk on" metric which states whether stocks are above/below a moving average
positions['risk_on'] = 0

for date in risk_on:
    if date in positions.index:
        positions['risk_on'].loc[date] = 1

neg_beta_currencies_pct = neg_beta_currencies_pct[positions.index[0]:]

# if market is risk off and currency is trending double the position size
for security in positions.columns:

    if security == 'risk_on':
        pass
    else:
        # if trend is up and stock market is risk off go 3-1 leverage
        positions.loc[(positions[security] == 1) & (positions['risk_on'] == 0), security] = 3
        # if trend is up and stock market is risk on go 1.5 - 1 leverage
        positions.loc[(positions[security] == 1) & (positions['risk_on'] == 1), security] = 1.5


trading = positions * neg_beta_currencies_pct

start = '2005'

trading = trading[start:]
neg_beta_currencies_pct = neg_beta_currencies_pct[start:]

data = np.cumprod(1 + neg_beta_currencies_pct)
trend_data = np.cumprod(1 + trading)



if __name__ == '__main__':
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(data, label='data')
    ax1.plot(trend_data, label='trend_data')
    ax1.set_yscale('log')
    plt.legend()
    plt.show()







