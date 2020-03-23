n=41
alive=[True]*(n+1) # alive[i] 为True，表示第i个人还或者，为False表示第i个人已死
# 注意我们声明了n+1个元素，以便使用1..n作为下标
dead_lst=[] # （按照自杀顺序）存放已死的人的编号
count = 0 # 保存目前的报数
i=0 # 目前是谁正在报数
while len(dead_lst)<n:
    #下一个人开始报数
    i+=1
    if i>n: # 如果已经到了圆圈的末尾，从头开始报数
        i=1
    if not alive[i]: #如果这个人已死，那么跳过他（尝试让下一个人报数）
        continue
    count+=1 # 让当前的人报下一个数
    if count == 3: # 报3，要自杀
        alive[i]=False
        dead_lst.append(i)
        count = 0

print(dead_lst)