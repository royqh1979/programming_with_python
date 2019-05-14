from dataclasses import dataclass


@dataclass()
class Student:
    id: str
    name: str
    class_name: str
    score: float