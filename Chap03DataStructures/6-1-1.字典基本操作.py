#注意，从python 3.7起，字典会保持其中元素加入的先后顺序

scores = {'张三':95, '李四':78, '王五': 82}
print(scores)
#获取王五的分数：
s=scores['王五']
print(f"王五的分数是{s}")

#增加郑六的分数
scores['郑六']=100
print(scores)
s=scores['郑六']
print(f"郑六的分数是{s}")

#迭代访问字典中所有元素
for key in scores:
    value = scores[key]
    print(f"scores[{key}]={value}")

# s=scores['孙七'] #会产生KeyError，因为scores字典中没有关键字为'孙七'的元素
s=scores.get('孙七',-1) #因为孙七不存在，所以返回所给的缺省值-1
print(f"孙七的分数是{s}")
s=scores.get('王五',-1) #因为王五存在，所以返回scores['王五']
print(f"王五的分数是{s}")

#修改王五的分数
scores['王五']=59
s=scores['王五']
print(f"王五的分数是{s}")

if '王五' in scores:
    print("ok")




