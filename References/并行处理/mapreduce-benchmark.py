from mapreduce import *
from math import ceil,sqrt

def mapper_2(item):
    return (item +5)*23 - 1


def reducer_2(accumulated, item):
    return accumulated + item


def timer(start):
    print('  Time       : %8.6fsec' % (time() - start))

def worker_assign(workers, current_worker_id, item):
    return item % workers == current_worker_id

def is_prime(n):
    for i in range(2,ceil(sqrt(n))):
        if n%i == 0:
            return False
    return True

if __name__ == "__main__":
    workers = 0
    N = 800000

    start = time()
    mr = MapReducer().workers(workers).prefilter(is_prime).mapper(mapper_2).reducer(reducer_2,0)
    result = mr(range(N))
    print('* map & reduce ')
    print('  MR Result  :', result)
    timer(start)

    start = time()
    mr = MapReducer().workers(workers).\
            prefilter(is_prime).mapper(mapper_2).reducer(reducer_2, 0).worker_assigner(worker_assign)
    result = mr(range(N))
    print('* map & reduce with work assign function ')
    print('  MR Result  :', result)
    timer(start)

    lst=list(range(N))
    start = time()
    n=sum([(n +5)*23 - 1 for n in range(N) if is_prime(n)])
    print('* Validation using list comprehension:',n)
    timer(start)
    start = time()
    n=0
    for i in range(N):
        if is_prime(i):
            n+=(i +5)*23 - 1
    print('* Validation using for loop:',n)
    timer(start)

    r=range(N)
    r=filter(is_prime,r)
    r=map(mapper_2,r)
    n=reduce(reducer_2,r)
    print('* Validation using for map filter reduce:', n)
    timer(start)



