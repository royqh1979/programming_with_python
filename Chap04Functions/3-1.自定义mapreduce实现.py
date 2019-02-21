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