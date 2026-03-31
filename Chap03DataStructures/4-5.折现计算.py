years=list(range(9))+[15,16,17,18,19,20,21,25]
deposits=[15350]*9+[-10000]*3+[-20000]*4+[-50000]
rate = 0.015
print(years,len(years))
print(deposits,len(deposits))
total=0
for year,deposit in zip(years,deposits):
    value = deposit / (1+rate)**year
    print(year,deposit,value)
    total += value
print(total)