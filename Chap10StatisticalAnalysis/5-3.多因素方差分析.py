import pandas as pd
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt

df = pd.read_csv("house-prices.csv", index_col=0)
print(df["Neighborhood"].value_counts())
print(df["Brick"].value_counts())
print(df.pivot_table(values="Price", index="Neighborhood",
                     columns="Brick", aggfunc="mean"))
df.boxplot("Price", "Brick")
plt.show()
df.boxplot("Price", "Neighborhood")
plt.show()
df["mix"] = df["Neighborhood"] + ":" + df["Brick"]
df.boxplot("Price", "mix")
plt.show()

from statsmodels.formula.api import ols
model = ols("Price ~ C(Brick) * C(Neighborhood)", data=df)
lm = model.fit()
print(lm.summary())

from statsmodels.stats.anova import anova_lm
print(anova_lm(lm))

