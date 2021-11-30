import numpy as np
import pandas as pd

import alocacao_recursos.price_data.symbols_lists as all_symbols

list_symbols = []
list_symbols_us = all_symbols.get_symbols_us()
for symbol in list_symbols_us:
    symbol = symbol[:-3]
    list_symbols.append(symbol)
list_symbols_br = all_symbols.get_symbols_br()
for symbol in list_symbols_br:
    symbol = symbol + ".SA"
    list_symbols.append(symbol)
list_symbols_index = all_symbols.get_symbols_index()
for symbol in list_symbols_index:
    list_symbols.append(symbol)

return_data = pd.read_csv("../price_data/return_data.csv")

first_asset_return_df = return_data[return_data["asset"] == list_symbols[0]]
filtred_first_asset_return_df = first_asset_return_df.filter(['Date', 'return'], axis=1)
merged_return_df = filtred_first_asset_return_df.rename({'return': list_symbols[0]}, axis=1)
for i in range(1, len(list_symbols)):
    symbol = list_symbols[i]
    print(symbol + "\t\t : " + str(i) + " / " + str(len(list_symbols)))
    asset_return_df = return_data[return_data["asset"] == symbol]
    if len(asset_return_df) > 0:
        filtred_asset_return_df = asset_return_df.filter(['Date', 'return'], axis=1)
        filtred_asset_return_df = filtred_asset_return_df.rename({'return': symbol}, axis=1)
        merged_return_df = pd.merge(merged_return_df, filtred_asset_return_df, how="outer", on="Date")

merged_return_df = merged_return_df.fillna(0)
merged_return_df.set_index(["Date"], inplace=True)
merged_return_df = merged_return_df.sort_index()
merged_return_df.to_csv("../price_data/organized_return_data.csv")

print("\n")

price_data = pd.read_csv("../price_data/us_br_index_stock_data.csv")

first_asset_price_df = price_data[price_data["asset"] == list_symbols[0]]
filtred_first_asset_price_df = first_asset_price_df.filter(['Date', 'Adj Close'], axis=1)
merged_price_df = filtred_first_asset_price_df.rename({'Adj Close': list_symbols[0]}, axis=1)
for i in range(1, len(list_symbols)):
    symbol = list_symbols[i]
    print(symbol + "\t\t : " + str(i) + " / " + str(len(list_symbols)))
    asset_price_df = price_data[price_data["asset"] == symbol]
    if len(asset_price_df) > 0:
        filtred_asset_price_df = asset_price_df.filter(['Date', 'Adj Close'], axis=1)
        filtred_asset_price_df = filtred_asset_price_df.rename({'Adj Close': symbol}, axis=1)
        merged_price_df = pd.merge(merged_price_df, filtred_asset_price_df, how="outer", on="Date")

merged_price_df.set_index(["Date"], inplace=True)
merged_price_df = merged_price_df.sort_index()
merged_price_df.to_csv("../price_data/organized_price_data.csv")

print(" END ! ")
