import pandas as pd
import numpy as np
df=pd.read_csv("default.csv",index_col="no")
print(df)
print(df["student"].value_counts())
print(df["default"].value_counts())

# 将default列转换为0-1变量
df["default"] = (df["default"] == "Yes") - 0
print(df["default"])

from statsmodels.formula.api import logit
model = logit("default ~ C(student) + income + balance", data=df)
res = model.fit()
print(res.summary())

print(" ---- odds ratio ---- ")
import numpy as np
print(np.exp(res.params))