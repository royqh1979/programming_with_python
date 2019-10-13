"""
n个数字的可重复排列

使用栈实现DFS（深度优先搜索）
"""

def perm(n):
    """
    n个变量，每个变量可以取1，2，3，……，m，共m个值

    求所有的方案
    :param m: 每个变量可以取的最大值
    :param n: 变量个数
    """
    global count
    stack = []
    stack.append([])
    while len(stack)>0:
        node = stack.pop()
        if len(node)==n: # 当前方案已经是可用方案
            count+=1
            print(node)
        else:
            for i in range(1,n+1): # 在当前方案基础上产生新的方案，并且加入到队列末尾
                new_node = node.copy()
                new_node.append(i)
                stack.append(new_node)


n=int(input("请输入n："))
count = 0
perm(n)

print(f"共{count}种方案")