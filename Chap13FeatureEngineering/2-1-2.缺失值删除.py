import pandas as pd

df=pd.read_csv("missing-values.csv")
print(df)

print(" -- 删除指定的列（特征） --")
#删除指定的列（特征）
df1 = df.drop(columns=["Math"])
print(df1)

print(" -- 删除指定的行（样本） --")
#删除指定的行（样本）
df1 = df.drop(index=[1])
print(df1)

print(" -- 删除所有含缺失值的列（特征） --")
#删除所有含缺失值的列（特征）
df1 = df.dropna(axis=1)
print(df1)

print(" -- 删除所有含缺失值的行（样本） --")
#删除所有含缺失值的行（样本）
df1 = df.dropna()
print(df1)
