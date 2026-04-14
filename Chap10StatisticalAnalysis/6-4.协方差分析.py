import matplotlib.pyplot as plt
import pandas as pd
df=pd.read_csv("house-prices.csv",index_col=0)
print(df)

#拟合回归模型
from statsmodels.formula.api import ols
model = ols("Price ~ SqFt + C(Brick) * C(Neighborhood)",data=df)
lm = model.fit()
print(lm.summary())

#计算ANOVA表
from statsmodels.stats.anova import anova_lm
print(anova_lm(lm).round(3))

