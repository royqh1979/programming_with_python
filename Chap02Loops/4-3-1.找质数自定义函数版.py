def is_prime(n):
    for factor in range(2,n):
        if n%factor == 0:
            return False
    return True

for n in range(2,201):
    if is_prime(n):
        print(n)
