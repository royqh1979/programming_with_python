n=41
alive=[True]*(n+1)
dead_lst=[]
count = 0
i=0
while len(dead_lst)<n:
    i+=1
    if i>n:
        i=1
    if not alive[i]:
        continue
    count+=1
    if count == 3:
        alive[i]=False
        dead_lst.append(i)
        count = 0

print(dead_lst)