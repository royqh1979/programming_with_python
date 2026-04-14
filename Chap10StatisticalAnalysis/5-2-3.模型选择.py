import numpy as np
import pandas as pd
import statsmodels.api as sm

# 生成数据
np.random.seed(42)
n = 100
X = np.random.randn(n, 5)
y = 2 + 3 * X[:, 0] + 1.5 * X[:, 1] + np.random.randn(n) * 0.5  # 真实只有2个变量重要

# 拟合不同复杂度的模型
results = []

for k in range(1, 6):  # 1到5个预测变量
    X_k = X[:, :k]
    X_k = sm.add_constant(X_k)

    model = sm.OLS(y, X_k).fit()

    results.append({
        'k': k,
        'SSE': model.ssr,
        'R2': model.rsquared,
        'R2_adj': model.rsquared_adj,
        'AIC': model.aic,
        'BIC': model.bic,
    })

df_results = pd.DataFrame(results)
print(df_results)