
def qsort(lst):
    def quick_sort(lst, p, r):
        if p>=r:
            return
        q = partition(lst, p, r)
        quick_sort(lst, p, q - 1)
        quick_sort(lst, q + 1, r)

    def partition(lst, p, r):
        x=lst[r]
        i=p-1
        for j in range(p,r):
            if lst[j]<x:
                i+=1
                lst[i],lst[j]=lst[j],lst[i]
        i+=1
        lst[i],lst[r]=lst[r],lst[i]
        return i

    quick_sort(lst,0,len(lst)-1)

lst = [25,46,78,32,82,12,97,65,37,91,48,100,23,54]
qsort(lst)
print(lst)