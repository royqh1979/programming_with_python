"""
n个数字的无重复排列

使用标志列表判重
"""
n=4
count = 0
flags= [0] * (n + 1)
for i1 in range(1, n + 1):
    flags[i1]=1
    for i2 in range(1, n + 1):
        if flags[i2]==1:
            continue
        flags[i2]=1
        for i3 in range(1, n + 1):
            if flags[i3]==1:
                continue
            flags[i3]=1
            for i4 in range(1, n + 1):
                if flags[i4]==1:
                    continue
                flags[i4]=1
                count+=1
                print(f"{i1},{i2},{i3},{i4}")
                flags[i4]=0
            flags[i3]=0
        flags[i2]=0
    flags[i1]=0


print(f"共{count}种方案")