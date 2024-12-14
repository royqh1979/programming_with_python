# 绘制平行四边形
n=5
m=10
for i in range(n):
    for j in range(i):
        print(' ',end='')
    for j in range(m):
        print('*',end='')
    print()