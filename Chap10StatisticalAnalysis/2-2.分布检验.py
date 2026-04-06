import numpy as np
import scipy.stats as stats

#产生实验数据，s1服从均匀分布，s2服从正态分布
s1=np.random.uniform(0,100,1000)
s2=np.random.normal(0,1,1000)

print("---- Anderson-Darling检验(正态分布) ----")
print(stats.anderson(s1,dist="norm"))
print(stats.anderson(s2,dist="norm"))


print("---- Kolmogorov-Smirnov检验(正态分布) ----")
print(stats.kstest(s1,stats.norm.cdf))
print(stats.kstest(s2,stats.norm.cdf))

print("---- Kolmogorov-Smirnov检验(均匀分布) ----")
print(stats.kstest(s1,stats.uniform.cdf, args=[np.min(s1),np.max(s1)]))
print(stats.kstest(s2,stats.uniform.cdf, args=[np.min(s2),np.max(s2)]))
