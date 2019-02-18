#创建空集合
s=set()

#向集合中加入元素
s.add('张三')
s.add('李四')
s.add('王五')
s.add('张三')

#判断元素是否在集合中
if '王五' in s:
    print("王五在s里")
else:
    print("不在s里")

#从集合中删除元素
s.discard('王五')
if '王五' in s:
    print("王五在s里")
else:
    print("不在s里")

#遍历集合中所有元素
for elem in s:
    print(elem)
