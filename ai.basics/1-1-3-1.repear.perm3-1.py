
def perm4():
    global count
    for a[4] in range(1, m + 1):
        count += 1
        print(f"{a[1]},{a[2]},{a[3]},{a[4]}")


m=int(input("请输入m："))
count = 0
a =[0]*5
for a[1] in range(1, m + 1):
    for a[2] in range(1, m + 1):
        for a[3] in range(1, m + 1):
            perm4()

print(f"共{count}种方案")