import alocacao_recursos.builders.historico_precos as hprice


time_frame = "D1"
start = "2011-01-01"
finish = "2021-11-01"


hprice.create_price_csv(start, finish)
hprice.create_merged_price_df()
hprice.create_return_csv()
hprice.create_return_pivot_table_csv()
hprice.create_price_pivot_table_csv()


print("\n \t --- END !")
