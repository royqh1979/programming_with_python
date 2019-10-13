"""
n个数字的无重复排列

使用集合判重

用列表存储方案
"""

def perm(i,n):
    global count
    for a[i] in range(1, n + 1):
        if a[i] in used:
            continue
        used.add(a[i])
        if i == n:
            count += 1
            print(a[1:n + 1])
        else:
            perm(i+1,n)
        used.remove(a[i])

n=int(input("请输入n:"))
count = 0
used=set()
a = [0]*(n+1)



perm(1,n)

print(f"共{count}种方案")