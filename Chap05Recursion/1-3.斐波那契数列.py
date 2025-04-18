
def fibonacci(n):
    if n<=2:
        return 1
    return fibonacci(n-1)+fibonacci(n-2)

n=int(input("请输入n:"))
result = fibonacci(n)
print(f"斐波那契数列的第{n}项为{result}")