from mapreduce import MapReducer
from math import ceil,sqrt
from time import time
from functools import reduce

def mapper_2(item):
    return (item +5)*23 - 1


def reducer_2(accumulated, item):
    return accumulated + item


def timer(start):
    print('  Time       : %8.6fsec' % (time() - start))


def is_prime(n):
    for i in range(2,min(ceil(sqrt(n))+1,n)):
        if n%i == 0:
            return False
    return True


if __name__ == "__main__":
    workers = 0
    N = 800000


    print('* map & reduce 使用并行处理 ')
    lst = range(N)
    start = time()
    mr = MapReducer().workers(workers).prefilter(is_prime).mapper(mapper_2).reducer(reducer_2,0)
    result = mr(lst)
    print('  MR Result  :', result)
    timer(start)

    print('* 使用列表推导式（list comprehension)')
    start = time()
    n=sum([(n +5)*23 - 1 for n in range(N) if is_prime(n)])
    print('  Result: ', n)
    timer(start)

    print('* 使用for循环:')
    start = time()
    n=0
    for i in range(N):
        if is_prime(i):
            n+=(i +5)*23 - 1
    print('  Result: ', n)
    timer(start)

    print('* 使用python内置map reduce函数:')
    r=range(N)
    r=filter(is_prime,r)
    r=map(mapper_2,r)
    n=reduce(reducer_2,r)
    print('  Result: ', n)
    timer(start)



