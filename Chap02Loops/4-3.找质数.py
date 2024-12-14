for n in range(2,201):
    #判断n是否是质数
    is_prime = True
    for factor in range(2,n):
        if n % factor == 0:
            is_prime = False
            break
    #如果n是质数，打印n
    if is_prime:
        print(n)
