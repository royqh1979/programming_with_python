import numpy as np
import pandas as pd

stock = pd.read_csv("AAPL 2006-2023.csv",index_col=0)
#将索引转化为时间型
stock.index = pd.to_datetime(stock.index)

#计算日收益率
stock_daily_return = np.log(stock["Close"] / stock["Close"].shift(1))
stock_daily_return = stock_daily_return.dropna()

#计算每个月的平均年化收益率
stock_return = 252*stock_daily_return.resample("ME").mean()
stock_return.index = stock_return.index.to_period("M")
print(stock_return)


# Step 2: Load the monthly three factors into a dataframe
# CSV columns: , Mkt-RF, SMB, HML, RF
# The first columns represents the date
# The first row contains the column names
ff_factors_monthly = pd.read_csv(
    "Fama_French_3Factors_monthly.csv", index_col=0
)
ff_factors_monthly.index = pd.to_datetime(ff_factors_monthly.index, format="%Y%m")
ff_factors_monthly.index = ff_factors_monthly.index.to_period("M")
print(ff_factors_monthly)
# Filter factor dates to match the asset
data = ff_factors_monthly[
    ff_factors_monthly.index.isin(stock_return.index)
].copy()

# Step 3: Calculate excess returns for the asset
data["Rs_Rf"] = stock_return - data["RF"]
print(data.describe())

import statsmodels.formula.api as sm

# Run the regression
model = sm.ols(" Q('Rs_Rf') ~ Q('Mkt-RF') + SMB +HML ",data=data)
lm = model.fit()
# Display the summary of the regression
print(lm.summary())
print("----预期收益率----")
print(ff_factors_monthly.iloc[-1])
print(lm.predict(ff_factors_monthly.iloc[-1]))