
def factorial(n):
    if n==0:
        return 1
    return n*factorial(n-1)

n=int(input("请输入n:"))
result = factorial(n)
print(f"{n}!={result}")