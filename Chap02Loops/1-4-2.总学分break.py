total=0
count=0
while True:
    credit=float(input(f"请输入第{count+1}门课的学分:"))
    if credit <= 0 :
        break
    total += credit
    count+=1

print(f"一共{count}门课，总学分为{round(total,1)}")
