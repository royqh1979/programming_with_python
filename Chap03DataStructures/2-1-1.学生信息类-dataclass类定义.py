#使用dataclass注解语法来定义数据类（仅有属性，无自定义方法的类)
#其语法比一般类定义更简便，因此本课程主要使用这种方式来定义数据类
from dataclasses import dataclass

@dataclass()
class Student:
    id: int
    name: str
    score: int

s1 = Student(1,'张三',50)
s2 = Student(2,'李四',70)
s1.score = 80
print(s1.id,s1.name,s1.score)
s3=s1
print(s3.id,s3.name,s3.score)

s1.name = '王五'
print(s3.id,s3.name,s3.score)

print(s1)
