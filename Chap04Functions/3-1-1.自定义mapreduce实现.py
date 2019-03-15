def map(fn,lst):
    new_lst = []
    for elem in lst:
        new_elem = fn(elem)
        new_lst.append(new_elem)
    return new_lst

def filter(fn,lst):
    new_lst = []
    for elem in lst:
        if fn(elem):
            new_lst.append(elem)
    return new_lst

def reduce(fn,lst,initial):
    result = initial
    for elem in lst:
        result = fn(result,elem)
    return result

def double(n):
    return n*2

def is_odd(n):
    return n%2==1

def add(a,b):
    return a+b

def hello(name):
    return f"{name},你好"


lst_a=list(range(10))
print(lst_a)
lst_b=['张三','李四','王五']

lst_c=map(double,lst_a)
print(lst_c)

lst_c = map(hello,lst_b)
print(lst_c)

lst_c = filter(is_odd,lst_a)
print(lst_c)

result = reduce(add,lst_a,0)
print(result)



