"""
n个数字的可重复排列

递归实现
"""
def perm(i, n):
    global count
    for a[i] in range(1, n + 1):
        if i==4:
            count += 1
            print(f"{a[1]},{a[2]},{a[3]},{a[4]}")
        else:
            perm(i + 1, n)

n=int(input("请输入n："))
count = 0
a =[0]*5
perm(1, n)

print(f"共{count}种方案")