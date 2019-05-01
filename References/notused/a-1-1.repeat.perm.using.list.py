"""
n个数字的可重复排列

使用全局列表来模拟栈，实现DFS（深度优先搜索）
"""
def perm(n):
    global count
    i = 1
    while i>=1:
        a[i]+=1
        if a[i]>n: # 第i个变量的所有可能取值都试过了，回退到第i-1个变量进行尝试
            a[i]=0
            i-=1
        else: # 第i个变量尝试了一个新的取值
            if i==n: # 产生了一个新的方案
                count += 1
                print(a[1:n + 1])
            else:
                i+=1 # 尝试第i+1个变量


n=int(input("请输入n："))
count = 0
a =[0]*(n+1)
perm(n)

print(f"共{count}种方案")