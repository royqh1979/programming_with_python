
def find_max(lst,n):
    if n==1:
        return lst[0]
    m=find_max(lst,n-1)
    if m>lst[n-1]:
        return m
    else:
        return lst[n-1]


lst = [25,46,78,32,82,12,97,65,37,91,48,100,23,54]
m=find_max(lst,len(lst))
print(f"最大值为{m}")