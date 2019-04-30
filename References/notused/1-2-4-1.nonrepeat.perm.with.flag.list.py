"""
n个数字的无重复排列

使用标志列表判重

使用函数
"""


def perm(i,n):
    global count
    for a[i] in range(1, n + 1):
        if flags[a[i]] == 1:
            continue
        flags[a[i]] = 1
        if i == n:
            count += 1
            print(a[1:n + 1])
        else:
            perm(i+1,n)
        flags[a[i]] = 0

n=int(input("请输入n："))
count = 0
flags= [0] * (n + 1)
a = [0] * (n+1)

perm(1,n)


print(f"共{count}种方案")