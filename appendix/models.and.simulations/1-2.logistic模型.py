from matplotlib import pyplot as plt

real_n = [3.93,5.31,7.24,9.64,12.87,17.07,23.19,31.44,38.56,50.16,
          62.95,76.00,91.99,105.71,122.76,131.67,150.70,179.32,203.21,226.51,
            248.71,281.42] # 美国真实人口数量，用于比较

N = (2000-1790)//10 # 迭代次数
n = [0]*(N+1)
years = [0]*(N+1)
r = 0.2743
n[0] = 3.93  # 1790年人口数，单位为百万
years[0] = 1790
n_m = 366.7066 # 人口上限
for i in range(1,N+1):
    rate=r*(1-n[i-1]/n_m)
    n[i]=n[i-1]+n[i-1]*rate
    years[i]=years[i-1]+10
plt.plot(years,n, marker='.',color='red')
plt.plot(years,real_n, marker='.',color='blue')
plt.show()