import numpy as np
from scipy.optimize import minimize
from scipy.stats import binom

n_samples = 1000
n_defaults = 5

result = minimize(
    fun=lambda p: -binom.logpmf(n_defaults,n_samples,p),
    x0=[0.5],  # 初始猜测
    bounds=[(0.001, 0.999)],  # 概率范围
    method='L-BFGS-B'
)
print("最大似然法估计违约率:",result.x)