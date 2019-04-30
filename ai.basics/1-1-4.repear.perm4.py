def perm(i, m):
    global count
    for a[i] in range(1, m + 1):
        if i==4:
            count += 1
            print(f"{a[1]},{a[2]},{a[3]},{a[4]}")
        else:
            perm(i + 1, m)

m=int(input("请输入m："))
count = 0
a =[0]*5
perm(1, m)

print(f"共{count}种方案")