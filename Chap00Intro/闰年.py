# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 18:19:21 2018

@author: Roy
"""

y = 2000

if (y % 100) == 0:
    if (y % 400) == 0:
        print(str(y) + "年是闰年")
    else:
        print(str(y) + "年不是闰年")
else:
    if (y % 4) == 0:
        print(str(y) + "年是闰年")
    else:
        print(str(y) + "年不是闰年")
