import numpy as np
import scipy.stats as stats

#产生实验数据，s1服从均匀分布，s2服从正态分布
s1=np.random.uniform(0,100,1000)
s2=np.random.normal(0,1,1000)

print("---- 峰度和偏度检验 ----")
print(stats.normaltest(s1))
print(stats.normaltest(s2))

print("---- Shapiro-Wilk检验 ----")
print(stats.shapiro(s1))
print(stats.shapiro(s2))

print("---- Jarque-Bera检验 ----")
print(stats.jarque_bera(s1))
print(stats.jarque_bera(s2))