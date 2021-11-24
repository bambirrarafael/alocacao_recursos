import requests
import json
import pandas as pd
import MetaTrader5 as mt5
import pandas_datareader as pdr


def pdr_get_and_save_prices(list_symbols, file_exit_name, start, finish, us_only=True):
    list_frames = []
    i = 0
    for symbol in list_symbols:
        if us_only:
            symbol = symbol[:-3]
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
    data.to_csv(file_exit_name)
    print("\n End seving " + file_exit_name + "\n")


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
