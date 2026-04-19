import pandas as pd
import statsmodels.formula.api as sm

data = pd.read_csv("house-prices.csv",index_col=0)
group1 = data[data["Neighborhood"] == "East"]
group2 = data[data["Neighborhood"] == "North"]
group3 = data[data["Neighborhood"] == "West"]

print(group1)
print(group2)
print(group3)

from scipy.stats import f_oneway
f_stat,p_value = f_oneway(
    group1["Price"], group2["Price"], group3["Price"])
print(f_stat,p_value)


