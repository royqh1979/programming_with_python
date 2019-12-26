from typing import List

# 更紧凑的next数组算法

def calc_next(s:str)->List[int]:
    """
    计算s字符串的next数组

    next[i]为s第i个字符前有多少个字符与字符串开头相同

    :param s: 要计算的字符串s
    :return: 对应的next数组
    """
    if s is None:
        raise ValueError("s is None!")
    if len(s)==0:
        return []
    s_next = [-1]*len(s)
    if len(s)==1:
        return s_next

    i=1
    j=-1
    while i<len(s):
        if j==-1 or s[i-1]==s[j]:
            j=j+1
        else:
            j = s_next[j]
            continue
        s_next[i] = j
        i += 1

    return s_next

print(calc_next("aabc_aabc"))