from time import perf_counter

def fibonacci(n):
    if n<=2:
        return 1
    return fibonacci(n-1)+fibonacci(n-2)

n=int(input("请输入n:"))
start_time = perf_counter()
result = fibonacci(n)
end_time = perf_counter()
print(f"斐波那契数列的第{n}项为{result}")
print(f"用时{end_time-start_time}秒")