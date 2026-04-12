import pandas as pd
import numpy as np

labels=['a','b','c','d','e']
a=np.arange(5)

#使用数据数组和标签列表建立Series对象
p1 = pd.Series(a,index=labels)
print("\np1")
print(p1)

#使用字典来建立Series对象
p2=pd.Series({'c':1,'b':2,'a':3,'z':100})
print("\np2")
print(p2)

#分别用数字下标、数据项名称下标、数据项（属性）名访问数据项：
print("p1['a']",p1['a'])
print("p1.a",p1.a)
print("p1.iloc[0]",p1.iloc[0])

# 和ndarray做基本运算，相当于两个ndarray做基本运算
print("a+p1",a+p1)
# 将series对象当ndarray做numpy中的函数的参数
print(np.sin(p1))
# 和另一个Series做运算，注意是同名项相互运算
print("p1+p2",p1+p2)

