"""
n个数字的可重复排列

使用栈实现回溯法搜索
"""
def perm(n):
    """
    n个变量，每个变量可以取1，2，3，……，m，共m个值

    求所有的方案
    :param m: 每个变量可以取的最大值
    :param n: 变量个数
    """
    global count
    solution = [0]*(n+1)
    i=1
    while True:
        solution[i] += 1 # 当前变量（栈顶变量）尝试下一个取值
        if solution[i]>n: # 当前变量的所有可能取值都试过了，丢弃该变量（循环后会尝试前一个变量）
            i-=1
            if i<1:
                break
            continue
        if i==n: # 产生了一个新的方案
            count += 1
            print(solution)
        else:
            i+=1 # 下一个变量从1开始尝试取值（因为循环后会+1）
            solution[i]=0


n=int(input("请输入n："))
count = 0
perm(n)

print(f"共{count}种方案")