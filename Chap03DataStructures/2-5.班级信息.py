from dataclasses import dataclass
from typing import List

# 前置声明，以便在Student定义中时使用Clazz
class Clazz:
    pass

@dataclass()
class Student:
    id:int
    name:str
    clazz:Clazz


@dataclass()
class Clazz:
    id:int
    name:str
    students:List[Student]

IM22=Clazz(2201,"信管22",[])
IM22.students.append(Student(220101,"张三", IM22))
IM22.students.append(Student(220102,"李四", IM22))
IM22.students.append(Student(220103,"王五", IM22))

print(IM22)
s1=IM22.students[0]
print(s1)
print(s1.clazz)

