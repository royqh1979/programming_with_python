class Student:
    def __init__(self,id,name,score):
        self.id=id
        self.name = name
        self.score = score


s1 = Student(1,'张三',50)
s2 = Student(2,'李四',70)
s1.score = 80
print(s1.name)
s3=s1
s1.name = '王五'
print(s3.name)