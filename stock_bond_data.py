import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import norgatedata
from datetime import datetime


# function to be used if a start_date is defined
def norgate_defined_start(watchlist, start_date, end_date, frequency):
    symbols = norgatedata.watchlist_symbols(watchlist)

    df_list = []

    for symbol in symbols:
        norgate_df = norgatedata.price_timeseries(
            symbol,
            start_date=start_date,
            end_date=end_date,
            interval=frequency,
            format='pandas-dataframe')

        # creating a symbol column so that we can identify
        # what ticker information we're looking at
        norgate_df['Symbol'] = symbol

        # appending the dataframes to an empty list to concatenate them after the for loop
        df_list.append(norgate_df)

    return df_list


# function to be used if a lookback period is specified
def norgate_interval_start(watchlist, end_date, lookback_period, frequency):
    symbols = norgatedata.watchlist_symbols(watchlist)

    df_list = []

    for symbol in symbols:
        norgate_df = norgatedata.price_timeseries(
            symbol,
            limit=lookback_period,
            end_date=end_date,
            interval=frequency,
            format='pandas-dataframe')

        # creating a symbol column so that we can identify
        # what ticker information we're looking at
        norgate_df['Symbol'] = symbol

        # appending the dataframes to an empty list to concatenate them after the for loop
        df_list.append(norgate_df)

    return df_list


def create_stock_dataframe(watchlist=None, start_date=None, end_date=None, lookback_period=None, frequency=None):
    if start_date is not None:

        df_list = norgate_defined_start(watchlist, start_date, end_date, frequency)

    elif lookback_period is not None:

        df_list = norgate_interval_start(watchlist, end_date, lookback_period, frequency)

    else:

        return ValueError('You must either pass a starting date or lookback period')

    print()

    appended_data = pd.concat(df_list)

    # just keep the closing data and the symbol
    appended_data.drop(['Open', 'High', 'Low', 'Volume', 'Open Interest',
                        'Delivery Month'], axis=1, inplace=True)

    portfolio_tickers = [i for i in appended_data['Symbol'].unique()]

    df_dict = {}

    for i in portfolio_tickers:
        df_data = appended_data['Close'][appended_data['Symbol'] == i]
        df_dict.update({i: df_data})

    final_df = pd.DataFrame(df_dict)

    return final_df


def create_index(start, end, index_ticker):
    symbol = index_ticker

    norgate_df = norgatedata.price_timeseries(symbol,
                                              start_date=start,
                                              end_date=end,
                                              interval='D',
                                              format='pandas-dataframe')

    norgate_df.drop(['Open', 'High', 'Low', 'Volume', 'Turnover',
                     'Unadjusted Close', 'Dividend'], axis=1, inplace=True)

    # changing name from Close to whatever the ticker is
    norgate_df.rename({'Close': index_ticker}, inplace=True, axis=1)

    # return the cumulative pct return over the period we have the data for
    norgate_df[index_ticker] = np.cumprod(1 + norgate_df[index_ticker].pct_change())

    return norgate_df


# Function Inputs
start = '1990-01-01'
end = '2020-12-31'
lookback_period = None
watchlist_name = 'stock_and_bond_futures'

securities_df = create_stock_dataframe(watchlist=watchlist_name,
                                       start_date=start,
                                       end_date=end,
                                       lookback_period=lookback_period,
                                       frequency='D')

# creating a daily pct_change version of the securities_df
securities_pct = securities_df.pct_change()

# keeping the date column in the data
securities_df['Date'], securities_pct['Date'] = securities_df.index, securities_pct.index

# # removing the Datetime index so that we can use .loc without SetWithCopyWarnings
# securities_df.reset_index(drop=True, inplace=True)
# securities_pct.reset_index(drop=True, inplace=True)

securities_df.drop({'Date'}, axis=1, inplace=True)
securities_pct.drop({'Date'}, axis=1, inplace=True)
securities_pct.fillna(0, inplace=True)

stocks_bonds_pct = securities_pct.copy()
stocks_bonds = securities_df.copy()

if __name__ == '__main__':

    data = np.cumprod(1 + securities_pct)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(data)
    ax1.set_yscale('log')
    plt.show()
