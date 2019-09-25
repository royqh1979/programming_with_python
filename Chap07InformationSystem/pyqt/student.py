from dataclasses import dataclass

@dataclass()
class Student:
    id: int
    name: str
    class_name: str
    score: float
