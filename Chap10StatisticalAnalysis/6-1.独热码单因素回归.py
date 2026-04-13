import pandas as pd

data = pd.read_csv("house-prices.csv",index_col=0)
print(pd.get_dummies(data["Neighborhood"], drop_first=True))

import statsmodels.formula.api as sm
model = sm.ols("Price ~ C(Neighborhood)", data=data)
lm = model.fit()
print(lm.summary())


