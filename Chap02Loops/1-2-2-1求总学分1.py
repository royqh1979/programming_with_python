#求总学分，用户直接输入课程门数
n=int(input("请输入有多少门课程："))
total = 0
i=1
while i<=n:
    score = float(input(f"请输入第{i}门课程的学分"))
    total += score
    i+=1
print(f"总学分是{total}")