import numpy as np
import pandas as pd

labels=['a','b','c','d','e']
a=np.arange(5)

#使用数据数组和标签列表建立Series对象
p1 = pd.Series(a,index=labels)
print("p1：",p1)

#使用字典来建立Series对象
p2=pd.Series({'c':1,'b':2,'a':3,'z':100})
print("p2:",p2)

#分别用数字下标、数据项名称下标、数据项（属性）名访问数据项：
print("p1[0]",p1[0])
print("p1['a']",p1['a'])
print("p1.a",p1.a)

# 和ndarray做基本运算，相当于两个ndarray做基本运算
print("a+p1",a+p1)
# 和另一个Series做运算，注意是同名项相互运算
print("p1+p2",p1+p2)
# 将series对象当ndarray做numpy中的函数的参数
print(np.sin(p1))


