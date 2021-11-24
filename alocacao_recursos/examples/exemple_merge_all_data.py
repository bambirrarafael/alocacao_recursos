import pandas as pd


df_us_1 = pd.read_csv("../price_data/yahoo_us_stock_1.csv")
df_us_2 = pd.read_csv("../price_data/yahoo_us_stock_2.csv")
df_us_3 = pd.read_csv("../price_data/yahoo_us_stock_3.csv")
df_us_4 = pd.read_csv("../price_data/yahoo_us_stock_4.csv")
df_us_5 = pd.read_csv("../price_data/yahoo_us_stock_5.csv")

df_br_1 = pd.read_csv("../price_data/yahoo_br_stock_1.csv")
df_br_2 = pd.read_csv("../price_data/yahoo_br_stock_2.csv")
df_br_3 = pd.read_csv("../price_data/yahoo_br_stock_3.csv")

price_data = pd.concat([df_us_1, df_us_2, df_us_3, df_us_4, df_us_5, df_br_1, df_br_2, df_br_3])
price_data.to_csv("us_br_stock_data.csv")

print(" END ! ")
