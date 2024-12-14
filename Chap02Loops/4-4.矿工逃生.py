import random

total_time = 0 #总逃生时间
n=500000 #实验次数
for i in range(n):
    #模拟每一名矿工的逃生过程
    escape_time = 0 #单次实验逃生时间
    while True:
        door = random.randint(1,3)
        if door == 1:
            escape_time += 2
            break
        elif door == 2:
            escape_time += 3
        elif door == 3:
            escape_time += 5
    total_time += escape_time
    #显示前20名矿工各自的逃生时间
    if i<20:
        print(f"矿工{i}的逃生时间为{escape_time}")
average = total_time / n
print(f"平均逃生时间为{average: .2f}小时")