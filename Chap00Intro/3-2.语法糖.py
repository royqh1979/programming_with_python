# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 15:00:07 2018

@author: Roy
"""

lst1=[1,2,3,4,5,6]

#计算lst1中所有奇数的平方，保存到lst2中
lst2=[]
for x in lst1:
    if x%2==1: 
        lst2.append(x**2)

print(lst2)

#计算lst1中所有奇数的平方，保存到lst3中
lst3=[x**2 for x in lst1 if x%2==1]

print(lst3)