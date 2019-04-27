import numpy as np
import statsmodels.api as sm

nsample = 100

#这里，我们想要 x1 的值从 0 到 10 等差排列。

x = np.linspace(0, 10, nsample)
# 使用 sm.add_constant() 在 array 上加入一列常项1。

X = sm.add_constant(x)

# 然后设置模型里的 β0,β1  β0,β1，这里要设置成 1,10 。

beta = np.array([1, 10])

# 然后还要在数据中加上误差项，所以生成一个长度为k的正态分布样本。

e = np.random.normal(size=nsample)

# 由此，我们生成反应项 y(t)。

y = np.dot(X, beta) + e

# 好嘞，在反应变量和回归变量上使用 OLS() 函数。

model = sm.OLS(y,X)

# 然后获取拟合结果。

results = model.fit()

# 再调取计算出的回归系数。

print(results.params)

# 当然，也可以将回归拟合的摘要全部打印出来。

print(results.summary(alpha=0.01))

# 预测x=15时y的值(区间预测，置信度为99%)

predication = results.get_prediction([1,15])

print(predication.summary_frame(alpha=0.01))