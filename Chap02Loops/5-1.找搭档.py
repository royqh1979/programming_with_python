count=0
for b in range(1,11):
    for g in range(1,21):
        count+=1
        print(f"第{count}号搭配方案：{b}号男生和{g}号女生")

print(f"总共有{count}种搭配方案")