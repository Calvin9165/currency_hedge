import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from currency_trend import currency_trading
from stock_bond_data import stocks_bonds_pct

start_date = currency_trading.index[0]

stocks_bonds_pct = stocks_bonds_pct[start_date:]

combined = pd.DataFrame(index=currency_trading.index, data=None)

for column in currency_trading.columns:
    combined[column] = currency_trading[column]

for column in stocks_bonds_pct.columns:
    combined[column] = stocks_bonds_pct[column]

stocks = '&SP'
bonds = '&ZN'

# combined.loc[(combined['risk_on']) == 1, stocks] *= 2
# combined.loc[(combined['risk_on']) == 0, stocks] *= 0.25

combined.drop('risk_on', axis=1, inplace=True)
combined[stocks] *= 6
combined[bonds] *= 10

combined['avg'] = combined.mean(axis=1)


data = np.cumprod(1 + combined)

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(data)
# ax1.set_yscale('log')
plt.show()

# for security in combined.columns:
#
#     if security == 'risk_on':
#         pass
#     else:
#         # if trend is up and stock market is risk off go 3-1 leverage
#         positions.loc[(positions[security] == 1) & (positions['risk_on'] == 0), security] = 3
#         # if trend is up and stock market is risk on go 1.5 - 1 leverage
#         positions.loc[(positions[security] == 1) & (positions['risk_on'] == 1), security] = 1.5


print(combined.head())
print(combined.tail())



