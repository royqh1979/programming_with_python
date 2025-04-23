def is_prime(x):
    if x<2:
        return False
    for i in range(2,x):
        if x % i ==0:
            return False
    return True

n=10
lst = [ x**2 for x in range(1,n+1) if is_prime(x) ]
print(lst)