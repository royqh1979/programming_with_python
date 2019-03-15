from easygraphics import dialog as dlg


class User:
    def __init__(self, id, name, borrowed, type):
        self.id = id
        self.name = name
        self.borrowed = borrowed
        self.type = type


def calc_books_can_borrow(user):
    if user.type == '教师':
        n = 10 - user.borrowed
    else:
        n = 5 - user.borrowed
    return n


data = dlg.get_many_strings("用户信息",
                            labels=['编号', '姓名', '已借数量', '类别'])

user_id = data[0]
name = data[1]
borrowed = int(data[2])
type = data[3]

user = User(user_id, name, borrowed, type)

can_borrow = calc_books_can_borrow(user)

dlg.show_message(f"用户{user.name}可以借{can_borrow}本书")
