import numpy as np
import scipy.stats as stats

s1=np.random.normal(0,1,1000)
s2=np.random.normal(0,2,1000)
s3=np.random.normal(0,1,2000)

print("---- Bartlett检验 ----")
print(stats.bartlett(s1,s2))
print(stats.bartlett(s1,s3))

print("---- Levene检验 ----")
print(stats.levene(s1,s2))
print(stats.levene(s1,s3))

print("---- Fligner-Killeen检验 ----")
print(stats.fligner(s1,s2))
print(stats.fligner(s1,s3))
