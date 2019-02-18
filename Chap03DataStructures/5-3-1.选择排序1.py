
def find_max(lst,start,end):
    """
    找从lst[start] 到 lst[end-1]之中的最大值下标
    :return: 最大值在lst中的下标
    """
    max = start
    for i in range(start,end):
        if lst[i] > lst[max]:
            max = i
    return max

def select_sort(lst):
    """
    选择排序

    :param lst: 要排序的列表
    """
    n = len(lst)
    for i in range(n):
        t = find_max(lst,i,n)
        lst[i],lst[t]=lst[t],lst[i]

lst=[15,20,4,20,76,58,95,32,63,60]
select_sort(lst)
print(lst)

