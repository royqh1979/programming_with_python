lst=[[1,2,3],[4,5,6],[7,8,9]]
print("lst[1]：",lst[1])
print("lst[1][1]：",lst[1][1])

# 建立一个3*5，元素全零的矩阵
# 错误的初始化方式
print("--错误的初始化方式--")
lst=[[0]*5]*3
print("初始化后：",lst)
lst[0][1]=3
print("修改lst[0][1]后：",lst)

# 正确的初始化方式
print("--正确的初始化方式--")
lst = [ [0]*5 for x in range(3)]
print(lst)
lst[0][1]=3
print("修改lst[0][1]后：",lst)
