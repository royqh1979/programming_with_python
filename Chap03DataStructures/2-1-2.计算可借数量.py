from dataclasses import dataclass

@dataclass()
class User:
    id: str
    name: str
    borrowed: int
    type: str


def calc_books_can_borrow(user):
    if user.type == '教师':
        n = 10 - user.borrowed
    else:
        n = 5 - user.borrowed
    return n

user_id = input("用户编号")
name = input("用户姓名")
borrowed = int(input("已借数量"))
type = input('类别')
user = User(user_id, name, borrowed, type)

can_borrow = calc_books_can_borrow(user)

dlg.show_message(f"用户{user.name}可以借{can_borrow}本书")
