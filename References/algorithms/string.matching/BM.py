# 使用Boyer-Moore算法查找子串
# 算法描述见https://www.cnblogs.com/lanxuezaipiao/p/3452579.html
from typing import List

def calc_bad_char_table(s:str)->List[int]:
    """
    计算坏字符表

    注：使用哈希表（字典）来保存字符在s中最后一次出现位置距s末尾的长度。如果字符在s中未出现，则字典中无其对应的位置信息
    :param s:
    :return:
    """
    bad_char={}
    for i in range(len(s)-1):
        ch = s[i]
        bad_char[ch]=len(s)-1-i
    return bad_char

def calc_suffix_table(s:str)->List[int]:
    """
    计算后缀表（暴力搜索版）

    suffix[i] 为s中以s[i]结尾的子串 和 s末尾的最长公共子串长度
    即，若m等于len(s)，l=suffix[i]
    则s[i-l+1]等于s[m-l+1],s[i-l+2]等于s[m-l+2]，……，s[i]等于s[m]，
    并且s[i-l]不等于s[m-l]
    :param s:
    :return:
    """
    suffix=[0]*len(s)
    suffix[-1]=len(s)
    for i in range(len(s)-1,-1,-1):
        l=0
        while i-l>=0 and s[i-l]==s[len(s)-1-l]:
            l+=1
        suffix[i]=l
    return suffix

print(calc_suffix_table("bcababab"))
