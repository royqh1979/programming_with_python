for n in range(2,201):
    is_prime = True
    for factor in range(2,n):
        if n % factor == 0:
            is_prime = False
            break
    if is_prime:
        print(n)
