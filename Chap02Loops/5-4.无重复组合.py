count=0
n=4
for i in range(1,n+1):
    for j in range(1,n+1):
        if i==j:
            continue
        for k in range(1,n+1):
            if i==k or j==k:
                continue
            count += 1
            print(f"第{count}种方案：甲担任{i}号课代表，乙担任{j}号课代表，丙担任{k}号课代表")

print(f"一共{count}种方案")