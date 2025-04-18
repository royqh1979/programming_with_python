
lst1=[1,2,3,4]
lst2=lst1
lst3=lst1.copy()
lst1.append(5)
lst1[0]=10
print(lst1,lst2,lst3)

dict1={'aaa':1,'bbb':2}
dict2=dict1
dict3=dict1.copy()
dict1['ccc']=3
print(dict1,dict2,dict3)

set1=set(['aaa','bbb','ccc'])
set2=set1
set3=set1.copy()
set1.add('ddd')
print(set1,set2,set3)
