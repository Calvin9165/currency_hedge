from load_currency_data import neg_beta_currencies_pct
from stock_bond_data import stocks_bonds_pct

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

index = neg_beta_currencies_pct.index

combined = pd.DataFrame(index=index)

for column in neg_beta_currencies_pct:
    combined[column] = neg_beta_currencies_pct[column]

for column in stocks_bonds_pct:
    combined[column] = stocks_bonds_pct[column]

combined.fillna(0, inplace=True)

if __name__ == '__main__':

    data = np.cumprod(1 + combined)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(data)
    ax1.set_yscale('log')
    plt.show()