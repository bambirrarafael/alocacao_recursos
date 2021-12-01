import requests
import json
import pandas as pd
import MetaTrader5 as mt5
import pandas_datareader as pdr
import alocacao_recursos.price_data.symbols_lists as all_symbols


def create_price_csv(start, finish, save_files=False, name_scenario=""):
    list_symbols_us = all_symbols.get_symbols_us()
    if len(list_symbols_us) > 0:
        print("\n \t --- Getting "+name_scenario+" US stock price data \n")
        try:
            list_symbols_us.remove("PBR.A.US")
        except:
            pass
        try:
            list_symbols_us.remove("VALE.P.US")
        except:
            pass
        try:
            price_us = pdr_get_and_save_prices(list_symbols_us, "../price_data/"+name_scenario+"yahoo_us_stock.csv",
                                               start, finish, save_files=save_files)
        except:
            price_us = None
    else:
        price_us = None
        print("\n \t --- No US data to get \n")
    #
    lista_symbols_br = all_symbols.get_symbols_br()
    if len(lista_symbols_br) > 0:
        print("\n \t --- Getting "+name_scenario+" BR stock price data \n")
        try:
            price_br = pdr_get_and_save_prices(lista_symbols_br, "../price_data/"+name_scenario+"yahoo_br_stock.csv",
                                               start, finish, us_only=False,  save_files=save_files)
        except:
            price_br = None
    else:
        price_br = None
        print("\n \t --- No BR data to get \n")
    #
    lista_symbols_index = all_symbols.get_symbols_index()
    if len(lista_symbols_index) > 0:
        print("\n \t --- Getting "+name_scenario+" index price data \n")
        try:
            price_index = pdr_get_and_save_prices(lista_symbols_index, "../price_data/"+name_scenario+"yahoo_index.csv",
                                                  start, finish, us_only=False, index=True, save_files=save_files)
        except:
            price_index = None
    else:
        price_index = None
        print("\n \t --- No Index data to get \n")
    #
    print("\n \t --- End of "+name_scenario+" getting data \n")
    return price_us, price_br, price_index


def create_merged_price_df(price_us=None, price_br=None, price_index=None, save_files=False, name_scenario=""):
    print("\n \t --- Creating merged price DataFrame \n")
    list_dfs = []
    if price_us is None:
        try:
            df_us_1 = pd.read_csv("../price_data/"+name_scenario+"yahoo_us_stock.csv")
            list_dfs.append(df_us_1)
        except:
            pass
    else:
        list_dfs.append(price_us)
    #
    if price_br is None:
        try:
            df_br_1 = pd.read_csv("../price_data/"+name_scenario+"yahoo_br_stock.csv")
            list_dfs.append(df_br_1)
        except:
            pass
    else:
        list_dfs.append(price_br)
    #
    if price_index is None:
        try:
            df_index = pd.read_csv("../price_data/"+name_scenario+"yahoo_index.csv")
            list_dfs.append(df_index)
        except:
            pass
    else:
        list_dfs.append(price_index)
    #
    price_data = pd.concat(list_dfs)
    if save_files:
        price_data.to_csv("../price_data/"+name_scenario+"us_br_index_stock_data.csv")
    #
    print("\n \t --- End of creating "+name_scenario+" merged price DataFrame \n")
    return price_data


def create_return_csv(price_data=None, save_files=False, name_scenario=""):
    print("\n \t --- Creating return csv \n")
    list_symbols_us = all_symbols.get_symbols_us()
    list_symbols_br = all_symbols.get_symbols_br()
    list_symbols_index = all_symbols.get_symbols_index()
    list_symbols = ajustar_nome_list_symbols(list_symbols_us, list_symbols_br, list_symbols_index)
    #
    if price_data is None:
        try:
            price_data = pd.read_csv("../price_data/"+name_scenario+"us_br_index_stock_data.csv")
        except:
            pass
    #
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
    #
    returns_data = pd.concat(list_df_returns)
    if save_files:
        returns_data.to_csv("../price_data/"+name_scenario+"return_data.csv")
    print("\n \t --- End of creating "+name_scenario+" return csv \n")
    return returns_data


def create_return_pivot_table_csv(return_data=None, save_files=False, name_scenario=""):
    print("\n \t --- Creating "+name_scenario+" return pivot table csv \n")
    list_symbols_us = all_symbols.get_symbols_us()
    list_symbols_br = all_symbols.get_symbols_br()
    list_symbols_index = all_symbols.get_symbols_index()
    list_symbols = ajustar_nome_list_symbols(list_symbols_us, list_symbols_br, list_symbols_index)
    #
    flag_no_saved_file = False
    if return_data is None:
        flag_no_saved_file = True
        try:
            return_data = pd.read_csv("../price_data/"+name_scenario+"return_data.csv")
        except:
            pass
    #
    first_asset_return_df = return_data[return_data["asset"] == list_symbols[0]]
    filtred_first_asset_return_df = first_asset_return_df.filter(['Date', 'return'], axis=1)
    merged_return_df = filtred_first_asset_return_df.rename({'return': list_symbols[0]}, axis=1)
    print(list_symbols[0] + "\t\t : " + str(0) + " / " + str(len(list_symbols)))
    for i in range(1, len(list_symbols)):
        symbol = list_symbols[i]
        print(symbol + "\t\t : " + str(i) + " / " + str(len(list_symbols)))
        asset_return_df = return_data[return_data["asset"] == symbol]
        if len(asset_return_df) > 0:
            filtred_asset_return_df = asset_return_df.filter(['Date', 'return'], axis=1)
            filtred_asset_return_df = filtred_asset_return_df.rename({'return': symbol}, axis=1)
            merged_return_df = pd.merge(merged_return_df, filtred_asset_return_df, how="outer", on="Date")
    #
    merged_return_df = merged_return_df.fillna(0)
    if flag_no_saved_file:
        merged_return_df.set_index(["Date"], inplace=True)
    merged_return_df = merged_return_df.sort_index()
    if save_files:
        merged_return_df.to_csv("../price_data/"+name_scenario+"organized_return_data.csv")
    print("\n \t --- End of creating "+name_scenario+" return pivot table csv \n")
    return merged_return_df


def create_price_pivot_table_csv(price_data=None, save_files=None, name_scenario=""):
    print("\n \t --- Creating "+name_scenario+" price pivot table csv \n")
    list_symbols_us = all_symbols.get_symbols_us()
    list_symbols_br = all_symbols.get_symbols_br()
    list_symbols_index = all_symbols.get_symbols_index()
    list_symbols = ajustar_nome_list_symbols(list_symbols_us, list_symbols_br, list_symbols_index)
    #
    flag_no_saved_file = False
    if price_data is None:
        flag_no_saved_file = True
        try:
            price_data = pd.read_csv("../price_data/"+name_scenario+"us_br_index_stock_data.csv")
        except:
            pass
    #
    first_asset_price_df = price_data[price_data["asset"] == list_symbols[0]]
    filtred_first_asset_price_df = first_asset_price_df.filter(['Date', 'Adj Close'], axis=1)
    merged_price_df = filtred_first_asset_price_df.rename({'Adj Close': list_symbols[0]}, axis=1)
    print(list_symbols[0] + "\t\t : " + str(0) + " / " + str(len(list_symbols)))
    for i in range(1, len(list_symbols)):
        symbol = list_symbols[i]
        print(symbol + "\t\t : " + str(i) + " / " + str(len(list_symbols)))
        asset_price_df = price_data[price_data["asset"] == symbol]
        if len(asset_price_df) > 0:
            filtred_asset_price_df = asset_price_df.filter(['Date', 'Adj Close'], axis=1)
            filtred_asset_price_df = filtred_asset_price_df.rename({'Adj Close': symbol}, axis=1)
            merged_price_df = pd.merge(merged_price_df, filtred_asset_price_df, how="outer", on="Date")
    #
    if flag_no_saved_file:
        merged_price_df.set_index(["Date"], inplace=True)
    merged_price_df = merged_price_df.sort_index()
    if save_files:
        merged_price_df.to_csv("../price_data/"+name_scenario+"organized_price_data.csv")
    print("\n \t --- End of creating "+name_scenario+" price pivot table csv \n")
    return merged_price_df


def pdr_get_and_save_prices(list_symbols, file_exit_name, start, finish, us_only=True, index=False, save_files=False):
    list_frames = []
    i = 1
    for symbol in list_symbols:
        if us_only:
            symbol = symbol[:-3]
        elif index:
            pass
        else:
            symbol = symbol + ".SA"
        print(symbol + "\t\t : " + str(i) + " / " + str(len(list_symbols)))
        i += 1
        try:
            df_price = pdr_get_asset_historic_price(symbol, start, finish)
            df_price['asset'] = symbol
            list_frames.append(df_price)
        except:
            continue
    data = pd.concat(list_frames)
    if save_files:
        data.to_csv(file_exit_name)
    print("\n End seving " + file_exit_name + "\n")
    return data


def pdr_get_asset_historic_price(symbol, start, finish):
    return pdr.DataReader(symbol, data_source='yahoo', start=start, end=finish)


def mt_get_and_save_prices(list_symbols, file_exit_name, time_frame, start, finish, account, password, server):
    list_frames = []
    i = 0
    for symbol in list_symbols:
        print(symbol + "\t\t : " + str(i) + " / " + str(len(list_symbols)))
        i += 1
        df_price = mt_get_asset_historic_price(symbol, time_frame, start, finish, str(account), password, server)
        df_price['asset'] = symbol
        if df_price["time"] is not None:
            list_frames.append(df_price)
    data = pd.concat(list_frames)
    data.to_csv(file_exit_name)
    print("\n End seving " + file_exit_name + "\n")


def mt_get_asset_historic_price(symbol, time_frame, start, finish, account, password, server):
    """

    :param symbol: (str)
    :param time_frame: (str)
    :param start: (str) %Y-$m-%d
    :param finish: (str)
    :param account: (str)
    :param password: (str)
    :param server: (str)
    :return:
    """
    url = "http://localhost:5000/get_historic_price"

    form_data = {'symbol': symbol,
                 'time_frame': time_frame,
                 'start': start,
                 'finish': finish,
                 'account': account,
                 'password': password,
                 'server': server}

    response = requests.post(url=url, data=form_data)

    response_dict = json.loads(response.content)
    df_price = pd.DataFrame(response_dict)
    df_price["time"] = pd.to_datetime(df_price["time"])
    return df_price


def get_asset_list(account, password, server, us_only=False):
    """

    :param account: (int)
    :param password: (str)
    :param server: (str)
    :return:
    """
    authorized = mt5.login(account, password=password, server=server)
    if authorized:
        print(mt5.account_info())
    else:
        print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
    lista_symbols_objects = mt5.symbols_get()
    lista_symbols = []
    for symbol_obj in lista_symbols_objects:
        if us_only:
            if symbol_obj.name.endswith(".US"):
                lista_symbols.append(symbol_obj.name)
        else:
            lista_symbols.append(symbol_obj.name)
    mt5.shutdown()
    return lista_symbols


def ajustar_nome_list_symbols(list_symbols_us, list_symbols_br, list_symbols_index):
    list_symbols = []
    for symbol in list_symbols_us:
        symbol = symbol[:-3]
        list_symbols.append(symbol)
    for symbol in list_symbols_br:
        symbol = symbol + ".SA"
        list_symbols.append(symbol)
    for symbol in list_symbols_index:
        list_symbols.append(symbol)
    return list_symbols
