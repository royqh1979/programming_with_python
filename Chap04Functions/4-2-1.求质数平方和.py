from math import sqrt,ceil

def is_prime(n):
    for i in range(2,n-1):
        if n%i == 0:
            return False
    return True

def square(n):
    return n**2

n=1000
lst = range(2,n+1)
lst = filter(is_prime,lst)
lst = map(square,lst)
result = sum(lst)
print(result)
