import numpy as np

print("--- 使用二维列表初始化 ----")
lst=[[1,2,3],[4,5,6],[7,8,9]]
a1=np.array(lst)
print("a1:",a1)
print("a1[1]",a1[1])
print("a1[1][1]",a1[1][1])

print("--- 使用 zeros() 创建全零数组 ---")
a1=np.zeros((5,5))
print("a1:",a1)

a1=np.identity(5)
print(a1)

print("--- 先创建一维数组，再用reshape()转换为多维数组 ---")
a1=np.arange(1,10).reshape((3,3))
print(a1)


