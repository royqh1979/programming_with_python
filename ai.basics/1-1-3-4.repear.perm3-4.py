"""
n个数字的可重复排列

已知n等于4
"""


def perm4():
    global count
    i = 4
    for a[i] in range(1, n + 1):
        if i == 4:
            count += 1
            print(f"{a[1]},{a[2]},{a[3]},{a[4]}")
        else:
            pass
            #perm5()


def perm3():
    global count
    i=3
    for a[i] in range(1, n + 1):
        if i==4:
            count += 1
            print(f"{a[1]},{a[2]},{a[3]},{a[4]}")
        else:
            perm4()

def perm2():
    global count
    i=2
    for a[i] in range(1, n + 1):
        if i==4:
            count += 1
            print(f"{a[1]},{a[2]},{a[3]},{a[4]}")
        else:
            perm3()

def perm1():
    global count
    i=1
    for a[i] in range(1, n + 1):
        if i==4:
            count += 1
            print(f"{a[1]},{a[2]},{a[3]},{a[4]}")
        else:
            perm2()


n=4
count = 0
a =[0]*5
perm1()

print(f"共{count}种方案")