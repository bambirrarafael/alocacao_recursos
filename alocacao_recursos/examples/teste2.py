import numpy as np
import pandas as pd
from alocacao_recursos.builders.portfolio_class import Portfolio
import alocacao_recursos.builders.analisador_portfolios as p_analizer


return_data = pd.read_csv("../price_data/organized_return_data.csv")
return_data = return_data.set_index(["Date"])
price_data = pd.read_csv("../price_data/organized_price_data.csv")
price_data = price_data.set_index(["Date"])

# cov_matrix = return_data.cov()
# corr_matrix = return_data.corr()

# scenario example
# i = return_data.index.get_loc('2020-01-02')
# return_data = return_data.iloc[i:i+100]

k = np.random.rand(len(return_data.columns))
x = k / sum(k)
p1 = Portfolio(x, return_data, nome_portfolio="p1")
p1.plot_histogram_portfolio_returns()
p1.plot_portfolio_cumulative_returns()
p1.print_asset_allocation()

p_analizer.plot_volatility_return([p1], return_data)

print("\n")
print(" END ! ")

