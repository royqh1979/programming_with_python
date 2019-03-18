def is_odd(n):
    return n%2 == 1

def is_even(n):
    return n%2 == 0

print('------------- Filter --------------')
lst_a = list(range(10))
print(lst_a)

lst_c = filter(is_odd,lst_a)
print(lst_c)
# filter返回的迭代器对象只能迭代一次
print("iteraction 1:")
for elem in lst_c:
    print(elem, end=" ")
print()
print("iteraction 2:")
for elem in lst_c:
    print(elem, end=" ")
print()

lst_c = filter(is_even,lst_a)
print(list(lst_c))
