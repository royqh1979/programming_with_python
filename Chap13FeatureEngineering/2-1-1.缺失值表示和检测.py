import pandas as pd

df=pd.read_csv("missing-values.csv")
print(df)
print(" -- DataFrame.isna() --")
print(df.isna())
print(" -- Series.isna() --")
print(df["Math"].isna())
print(" -- 找出哪些列中有缺失值 -- ")
print(df.isna().any())
print(" -- 找出哪些行中有缺失值 -- ")
print(df.isna().any(axis=1))