import numpy as np
import pandas as pd

import alocacao_recursos.sumilation.scenario_simulation as sim
import alocacao_recursos.builders.historico_precos as hprice

nome_s1 = "s1_"
start_s1 = "2020-01-01"
finish_s1 = "2021-11-30"
list_times_s1 = [(start_s1, finish_s1)]
return_data_s1, price_data_s1 = sim.get_return_data(list_times_s1, timeframe="D1", save_files=True, name_scenario=nome_s1)

nome_s2 = "s2_"
start_s2_a = "2020-02-01"
finish_s2_a = "2020-05-31"
start_s2_b = '2008-02-01'
finish_s2_b = '2008-05-31'
start_s2_c = '2015-05-01'
finish_s2_c = '2015-12-31'
list_times_s2 = [(start_s2_a, finish_s2_a), (start_s2_b, finish_s2_b), (start_s2_c, finish_s2_c)]
return_data_s2, price_data_s2 = sim.get_return_data(list_times_s2, timeframe="D1", save_files=True, name_scenario=nome_s2)

nome_s3 = "s3_"
start_s3_a = "2004-04-01"
finish_s3_a = "2008-05-01"
start_s3_b = "2016-06-01"
finish_s3_b = "2019-12-31"
list_times_s3 = [(start_s3_a, finish_s3_a), (start_s3_b, finish_s3_b)]
return_data_s3, price_data_s3 = sim.get_return_data(list_times_s3, timeframe="D1", save_files=True, name_scenario=nome_s3)

nome_s4 = "s4_"
start_s4 = "2010-01-01"
finish_s4 = "2015-12-31"
list_times_s4 = [(start_s4, finish_s4)]
return_data_s4, price_data_s4 = sim.get_return_data(list_times_s4, timeframe="D1", save_files=True, name_scenario=nome_s4)


s1 = sim.build_scenario(return_data_s1, nome_s1, 10000, price_data_s1, 63)
s2 = sim.build_scenario(return_data_s2, nome_s2, 10000, price_data_s2, 63)
s3 = sim.build_scenario(return_data_s3, nome_s3, 10000, price_data_s3, 63)
s4 = sim.build_scenario(return_data_s4, nome_s4, 10000, price_data_s4, 63)

list_scenarios = [s1, s2, s3, s4]
sim.plot_scenarios(list_scenarios)

for s in list_scenarios:
    print(s.scenario_name)
    s.list_eval_portfolios[0].print_asset_allocation()
    print("\n")

return_data = pd.read_csv("../price_data/organized_return_data.csv")
merged_return_df = return_data.set_index(["Date"])
price_data = pd.read_csv("../price_data/organized_price_data.csv")
price_data = price_data.set_index(["Date"])





print("\n")
print(" END ! ")

