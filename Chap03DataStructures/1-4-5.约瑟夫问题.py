n=41
alive=[1]*(n+1) # alive[i] 为1，表示第i个人还或者，为0表示第i个人已死
# 注意我们声明了n+1个元素，以便使用1..n作为下标
dead_lst=[] # （按照自杀顺序）存放已死的人的编号
count = 0 # 保存目前的报数
i=0 # 目前是谁正在报数
while len(dead_lst)<n:
    # 该谁报数了
    i+=1
    if i>n: # 如果已经到了圆圈的末尾，从第一个人重新开始
        i=1
    if alive[i]: #如果这个人还活着，让他/她报数
        count+=1 # 该报几了
        if count > 3: #超过3，从1重新开始
            count = 1
        if count == 3: # 报3，要自杀
            alive[i]=0
            dead_lst.append(i)

print(dead_lst)