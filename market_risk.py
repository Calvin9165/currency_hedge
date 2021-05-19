from stock_bond_data import stocks_bonds

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

risk_asset = '&SP'
lookback = 200

# stocks_bonds.plot()
# plt.show()

stocks_bonds['sma'] = 0
stocks_bonds['position'] = 0

stocks_bonds['sma'] = stocks_bonds[risk_asset].rolling(lookback).mean()
stocks_bonds.loc[stocks_bonds[risk_asset].shift(1) > stocks_bonds['sma'], 'position'] = 1

stocks_bonds.dropna(axis=0, inplace=True)


risk_on = stocks_bonds.loc[stocks_bonds['position'] == 1].index

# dates where we want the portfolio to be "risk on"
print(risk_on)


# stocks_bonds['test'] = 0
# stocks_bonds['test'].loc[risk_on] = 2
#
# stocks_bonds