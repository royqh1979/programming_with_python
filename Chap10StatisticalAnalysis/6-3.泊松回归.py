import pandas as pd

df = pd.read_csv("medpar.csv")

import statsmodels.formula.api as sm

model = sm.poisson("los ~ hmo + white + type2 + type3", data=df)
lm = model.fit()
print(lm.summary())