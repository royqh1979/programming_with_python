import numpy as np
import pandas as pd
from statsmodels.formula.api import ols

data = pd.read_csv("招商银行A股与沪深300指数日收盘价数据（2017-2020年）.csv",
                   encoding="GBK",index_col=0)
data_index = np.log(data / data.shift(1))
data_index = data_index.dropna()
print(data_index.describe())

model = ols("招商银行 ~ 沪深300指数", data=data_index)
lm=model.fit()
print(lm.summary())

beta = lm.params["沪深300指数"]
Rf=0.0385
Rm=252*data_index["沪深300指数"].mean()
Ri=Rf+beta*(Rm-Rf)
print("="*10)
print(f"招商银行A股的年化预期收益率{Ri*100:.2f}%")


