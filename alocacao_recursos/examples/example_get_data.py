import alocacao_recursos.builders.historico_precos as hprice


time_frame = "D1"
start = "2020-02-01"
finish = "2020-04-01"


price_us, price_br, price_index = hprice.create_price_csv(start, finish, save_files=False)
price_data = hprice.create_merged_price_df(price_us, price_br, price_index, save_files=False)
return_data = hprice.create_return_csv(price_data, save_files=False)
merged_return_df = hprice.create_return_pivot_table_csv(return_data, save_files=True)
merged_price_df = hprice.create_price_pivot_table_csv(price_data, save_files=True)


print("\n \t --- END !")
