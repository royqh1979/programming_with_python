#使用一般的类定义语法定义Student类
#注意与使用dataclass注解定义数据类时在语法上的区别
#本课主要使用dataclass注解语法来定义类，因为其更简便

class Student:
    def __init__(self,id,name,score):
        '''
        构造函数
        创建对象时会自动调用这个函数，以保证新对象的属性有正确的初始值。
        第一个参数self指向新创建的Student对象。

        :param id:
        :param name:
        :param score:
        '''
        self.id = id
        self.name = name
        self.score =score

s1 = Student(1,'张三',50)
s2 = Student(2,'李四',70)
s1.score = 80
print(s1.id,s1.name,s1.score)
s3=s1
print(s3.id,s3.name,s3.score)

#在运行之前可以猜猜print出来的s3.name的值是什么
s1.name = '王五'
print(s3.id,s3.name,s3.score)

#请注意实际print出的内容
print(s1)
print(s3)