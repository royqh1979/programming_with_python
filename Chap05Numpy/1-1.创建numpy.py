import numpy as np

#基于列表创建ndarray
a1=np.array([1,2,3,4,5,6])
print(a1)

#创建一个包含5个1的ndarray
a2=np.ones(5)
print(a2)

#创建一个包含5个0的ndarray
a3=np.zeros(5)
print(a3)

#创建一个包含20个从1一直到5，均匀分隔的数字的ndarray
a4=np.linspace(1,5,20)
print(a4)

#类似于python的range函数
a5=np.arange(5)
print(a5)

a6=np.arange(1,5)
print(a6)



#创建从