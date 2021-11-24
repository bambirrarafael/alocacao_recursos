import numpy as np
import pandas as pd
import scipy.optimize as opt

limite_financeiro = 10000

df1 = pd.read_csv("C:/Users/T-Gamer/Desktop/IBOV_psr_pVPA.csv", sep=",", encoding="latin-1")
df2 = pd.read_csv("C:/Users/T-Gamer/Desktop/ibov_LPA_ROA.csv", sep=",", encoding="latin-1")
dados = pd.DataFrame()

dados["ativo"] = df1["Ativo"]
dados["data"] = df1["Data"]
dados["psr"] = df1['PSR|Em moeda orig|no exercício|consolid:sim*']
dados["p_vpa"] = df1['P/VPA|Em moeda orig|consolid:sim*']

print("\n")


