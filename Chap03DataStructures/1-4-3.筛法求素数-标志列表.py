#筛法求素数（使用标志列表）

n=100
# 产生包含n+1个元素的列表
# 其中griddle[i]为0表示i不在筛中
#              为1表示i在筛中
# 开始时griddle全部元素均为1，即2...n都在筛中
griddle=[1]*(n+1)

#当前数字，从2开始
current=2
while current<=n:
    # current在筛中？
    if griddle[current]==1:
        x=current*2
        while x<=n:
            griddle[x]=0 #将x从筛中删除
            x+=current
    # 尝试下一个数
    current+=1

#将标志数组转换为普通数组
result = []
for i in range(2,n+1):
    #如果i在筛中，将其放入result列表
    if griddle[i]==1:
        result.append(i)
print(result)