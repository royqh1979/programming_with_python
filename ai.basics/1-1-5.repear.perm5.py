def do_perm(i, m, n):
    """
    n个变量，每个变量可以取1，2，3，……，m，共m个值

    求所有的方案

    :param i: 第i个变量下标
    :param m: 每个变量可以取的最大值
    :param n: 变量个数
    :return:
    """
    global count
    for a[i] in range(1, m + 1):
        if i==n:
            count += 1
            print(a[1:n+1])
        else:
            do_perm(i + 1, m, n)

def perm(m,n):
    """
    n个变量，每个变量可以取1，2，3，……，m，共m个值

    求所有的方案
    :param m: 每个变量可以取的最大值
    :param n: 变量个数
    """
    do_perm(1,m,n)

n=int(input("请输入n："))
m=int(input("请输入m："))
count = 0
a =[0]*(n+1)
perm(m, n)

print(f"共{count}种方案")