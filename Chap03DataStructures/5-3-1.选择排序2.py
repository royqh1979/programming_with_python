def select_sort(lst):
    """
    选择排序

    :param lst: 要排序的列表
    """
    n = len(lst)
    for i in range(n):
        t = i # lst[i]到lst[n-1]中最大值下标
        for j in range(i, n):
            if lst[j] > lst[t]:
                t = j
        #交换lst[i]和lst[t]，交换待排序部分的第一个元素和最大值元素
        lst[i],lst[t]=lst[t],lst[i]

lst=[15,20,4,20,76,58,95,32,63,60]
select_sort(lst)
print(lst)

