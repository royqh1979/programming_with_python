
stack = []

stack.append(-1)

while len(stack)>0:
    if stack[-1] == -1:
        stack[-1] = 1
    else:
        stack[-1] +=1
    if stack[-1]>4:
        stack.pop()
        continue
    else:
        if len(stack)==4:
            print(stack)
        else:
            stack.append(-1)