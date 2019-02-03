count=0
n=4
for i in range(1,n+1):
    for j in range(i+1,n+1):
        for k in range(j+1,n+1):
            count += 1
            print(f"第{count}种组合方案：{i}，{j}，{k}")

print(f"一共{count}种方案")