#
# 使用KMP算法进行子串匹配
#
# 算法说明参考
# https://blog.csdn.net/qq_37969433/article/details/82947411
from typing import List



def calc_next(s:str) -> List[int]:
    """
    计算next数组
    :param s:
    :return:
    """
    next=[0]*len(s)
    for i in range(len(s)):
        if i==0:
            next[i]=-1
            continue
        elif i==1:
            next[i]=0
        j=i-1
        while j>=0:
            if s[i-1]==s[next[j]]:
                next[i]=next[j]+1
                break
            else:
                j=next[j]
        if j<0:
            next[i]=0
    return next

def calc_next2(s:str) -> List[int]:
    """
    计算next数组(更紧凑算法）
    :param s:
    :return:
    """
    if len(s)==0:
        return []
    next=[0]*len(s)
    next[0]=-1
    if len(s)==1:
        return next
    next[1]=0
    i=2
    j=0
    while i<len(s):
        if s[i-1]==s[j]:
            next[i]=j+1
            i+=1
            j+=1
        else:
            j=next[j]
            if j==-1:
                next[i]=0
                i+=1
                j=0
    return next


def search(s1:str,s2:str)->int:
    """
    Search s1 in s2
    :param s1:
    :param s2:
    :return:
    """
    next=calc_next(s1)
    start = 0
    j=0
    while True:
        while start+j<len(s2) and j<len(s1) and s2[start+j] == s1[j]:
            j+=1
        if j==len(s1): # found!
            return start
        elif start+j>=len(s2): # not found!
            return -1
        else: #滑动准备下次匹配
            if j==-1: #如果是字串第一个字符
                start+=1
                j=0
            else: #滑动起始位置
                temp=j
                j=next[j]
                start=start+temp-j

s1="abcabaaaabaabcac"
s2="aabc_aabc"

next=calc_next(s2)
print(next)
next=calc_next2(s2)
print(next)
print(search(s2,s1))

s3="abcdabcefabcdabcdf"

next=calc_next(s3)
print(next)
next=calc_next2(s3)
print(next)

