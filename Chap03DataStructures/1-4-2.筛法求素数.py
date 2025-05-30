#筛法求素数
n=100
# 产生一个包含2到n所有整数列表（筛子列表)
lst=list(range(2, n + 1))

#当前元素下标
i=0
while i<len(lst):
    c=lst[i]
    # 从筛列表中删除c的所有倍数（current本身不删除）
    # 因为从列表中删除元素会导致后面元素的下标变化，所以应从后向前删
    # 注意range(a,b,-1)函数实际产生的序列是从a到b+1，不含b
    for j in range(len(lst) - 1, i, -1):
        #下标i从列表的最后一个元素开始,删除到当前元素为止（当前元素不删）
        if lst[j] % c == 0: #判断下表为i的元素是否是当前元素的倍数
            del lst[j]
    #当前元素下标+1，即取筛列表中的下一个元素
    i+=1
print(lst)
