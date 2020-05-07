"""
n个数字的可重复排列

递归实现
"""
def perm(i, n):
    global count
    for a[i] in range(1, n + 1):
        if i==n:
            count += 1
            # 显示输出找到的新排列
            for j in range(1,n+1):
                print(f"{a[j]}," ,end="")
            print()
        else:
            perm(i + 1, n)

n=int(input("请输入n："))
count = 0
a =[0]*5
perm(1, n)

print(f"共{count}种方案")