count=0
n=4
for i in range(1,n+1):
    for j in range(1,n+1):
        for k in range(1,n+1):
            count += 1
            print(f"第{count}种方案：甲加入{i}号社团，乙加入{j}号社团，丙加入{k}号社团")

print(f"一共{count}种方案")