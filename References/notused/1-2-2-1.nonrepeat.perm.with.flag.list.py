"""
n个数字的无重复排列

使用标志列表判重

用列表存储方案
"""
n=4
count = 0
flags= [0] * (n + 1)
a = [0] * (n+1)
for a[1] in range(1, n + 1):
    flags[a[1]]=1
    for a[2] in range(1, n + 1):
        if flags[a[2]]==1:
            continue
        flags[a[2]]=1
        for a[3] in range(1, n + 1):
            if flags[a[3]]==1:
                continue
            flags[a[3]]=1
            for a[4] in range(1, n + 1):
                if flags[a[4]]==1:
                    continue
                flags[a[4]]=1
                count+=1
                print(a[1:n+1])
                flags[a[4]]=0
            flags[a[3]]=0
        flags[a[2]]=0
    flags[a[1]]=0


print(f"共{count}种方案")