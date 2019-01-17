# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:20:02 2018

@author: Roy
"""
from datetime import datetime


def sum(n):
    s = 0
    for i in range(1, n + 1):
        s = s + i
    return s


begin = datetime.now()
t = 0
for i in range(1000):
    t = t + sum(100000)
end = datetime.now()
elapsed = end - begin

print(elapsed)
print("t=" + str(t));
