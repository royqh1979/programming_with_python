from matplotlib import pyplot as plt

real_n = [64,166.8,362.9,685.3,1323,2386, 4330,
          8453,14522,20661,26869,33482,39342.8]

N = 2005-1993 # 迭代次数
n = [0]*(N+1)
years = [0]*(N+1)
# m = 44436.41
# p = 0.0101
# q = 0.6354
q,m,p = 0.6354658463017459, 44327.330143238105, 0.010151647968018707
n[0] = 64
years[0] = 1993
for i in range(1,N+1):
    n[i]=n[i-1] + p*(m-n[i-1]) + q*n[i-1]/m*(m-n[i-1])
    years[i]=years[i-1]+1
print(n)
print(real_n)
plt.plot(years,n, marker='.',color='red')
plt.plot(years,real_n, marker='.',color='blue')
plt.show()