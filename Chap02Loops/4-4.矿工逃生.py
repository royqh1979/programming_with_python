import random

random.seed()
total_time = 0
n=500000

for i in range(n):
    escape_time = 0
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

average = total_time / n
print(f"平均逃生时间为{average: .2f}小时")