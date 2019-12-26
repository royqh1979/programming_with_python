# 使用Boyer-Moore算法查找子串
# 算法描述见https://www.cnblogs.com/lanxuezaipiao/p/3452579.html
from typing import List, Dict


def calc_bad_char_table(s:str)->Dict[str,int]:
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

def calc_good_table(s:str)->List[int]:
    """
    计算“好”后缀移动数组
    :param s:
    :return:
    """
    suffix = calc_suffix_table(s)

    # case 3
    good_table = [len(s)]*len(s)

    # case 2
    for i in range(len(s)-1,-1,-1):
        if suffix[i]==i+1:
            for j in range(0,len(s)-1-i):
                if good_table[j]==len(s):
                    good_table[j]=len(s)-1-suffix[i]
    #case 3
    for i in range(len(s)-1):
        good_table[len(s)-1-suffix[i]]=len(s)-1-i

    return good_table

def search(s1:str,s2:str)->int:
    bad_char_table=calc_bad_char_table(s2)
    good_table = calc_good_table(s2)
    i=0
    while i<=len(s1)-len(s2):
        print(i)
        j=len(s2)-1
        while j>=0:
            if s1[i+j]==s2[j]:
                j-=1
            else:
                break
        if j<0:
            return i
        m1=j-len(s2)+1+bad_char_table.get(s1[i+j],len(s2))
        m2=good_table[j]
        m=max(m1,m2,1)
        i+=m
    return None


print(calc_suffix_table("bcabcabcab"))
print(calc_good_table("bcabcabcab"))
print(search("abcbbacbabacab","babac"))
