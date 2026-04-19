import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Advertising.csv")
print(df.corr())

pd.plotting.scatter_matrix(df)
plt.show()

from statsmodels.formula.api import ols
model = ols("Sales ~ TV + Radio + Newspaper", data=df)
lm = model.fit()
print(lm.summary())

print("===== VIF =====")
#计算每个系数的VIF
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
for i in range(len(lm.model.exog_names)):
    print(lm.model.exog_names[i],vif(lm.model.exog,i))

