"""
n个数字的可重复排列

已知n等于4
"""
def perm4():
    global count
    for a[4] in range(1, n + 1):
        count += 1
        print(f"{a[1]},{a[2]},{a[3]},{a[4]}")


n=4
count = 0
a =[0]*5
for a[1] in range(1, n + 1):
    for a[2] in range(1, n + 1):
        for a[3] in range(1, n + 1):
            perm4()

print(f"共{count}种方案")