import pandas as pd

import alocacao_recursos.price_data.symbols_lists as all_symbols
import alocacao_recursos.builders.historico_precos as hprice

list_symbols = []
list_symbols_us = all_symbols.get_symbols_us()
list_symbols_br = all_symbols.get_symbols_br()
list_symbols_index = all_symbols.get_symbols_index()
list_symbols = hprice.ajustar_nome_list_symbols(list_symbols_us, list_symbols_br, list_symbols_index)


price_data = pd.read_csv("../price_data/us_br_index_stock_data.csv")

i = 1
list_df_returns = []
for symbol in list_symbols:
    print(symbol + "\t\t : " + str(i) + " / " + str(len(list_symbols)))
    i += 1
    asset_price_df = price_data[price_data["asset"] == symbol]
    if len(asset_price_df) > 0:
        if symbol in list_symbols_index or asset_price_df["Volume"].mean() > 1000000:
            filtred_asset_price_df = asset_price_df.filter(["Date", "Adj Close", "asset"])
            filtred_asset_price_df["return"] = filtred_asset_price_df["Adj Close"].pct_change()
            filtred_asset_price_df.dropna(inplace=True)
            list_df_returns.append(filtred_asset_price_df)
        else:
            print(" ----- OUT: " + symbol)

returns_data = pd.concat(list_df_returns)
returns_data.to_csv("../price_data/return_data.csv")

print("\n")
print(" END ! ")
