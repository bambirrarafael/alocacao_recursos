import pandas as pd
import MetaTrader5 as mt5
import alocacao_recursos.price_data.symbols_lists as all_symbols
import alocacao_recursos.builders.historico_precos as hprice



time_frame = "D1"
start = "2011-01-01"
finish = "2021-11-01"

list_symbols_us = all_symbols.get_symbols_us()
list_symbols_us.remove("PBR.A.US")
list_symbols_us.remove("VALE.P.US")
list_1 = list_symbols_us[0:100]
list_2 = list_symbols_us[100:200]
list_3 = list_symbols_us[200:300]
list_4 = list_symbols_us[300:400]
list_5 = list_symbols_us[400:-1]
hprice.pdr_get_and_save_prices(list_1, "../price_data/yahoo_us_stock_1.csv", start, finish)
hprice.pdr_get_and_save_prices(list_2, "../price_data/yahoo_us_stock_2.csv", start, finish)
hprice.pdr_get_and_save_prices(list_3, "../price_data/yahoo_us_stock_3.csv", start, finish)
hprice.pdr_get_and_save_prices(list_4, "../price_data/yahoo_us_stock_4.csv", start, finish)
hprice.pdr_get_and_save_prices(list_5, "../price_data/yahoo_us_stock_5.csv", start, finish)


lista_symbols_br = all_symbols.get_symbols_br()

br_list_1 = lista_symbols_br[0:50]
br_list_2 = lista_symbols_br[50:100]
br_list_3 = lista_symbols_br[100:-1]

hprice.pdr_get_and_save_prices(br_list_1, "../price_data/yahoo_br_stock_1.csv", start, finish, us_only=False)
hprice.pdr_get_and_save_prices(br_list_2, "../price_data/yahoo_br_stock_2.csv", start, finish, us_only=False)
hprice.pdr_get_and_save_prices(br_list_3, "../price_data/yahoo_br_stock_3.csv", start, finish, us_only=False)


lista_symbols_index = all_symbols.get_symbols_index()

hprice.pdr_get_and_save_prices(lista_symbols_index, "../price_data/yahoo_index.csv", start, finish, us_only=False, index=True)

print(" END ! ")
