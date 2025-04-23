from time import perf_counter

F=[0]*1000

def fibonacci(n):
    if (F[n]!=0):
        return F[n]
    if (n<=2) :
        F[n]=1
    else:
        F[n]=fibonacci(n-1)+fibonacci(n-2)
    return F[n]


n=int(input("请输入n:"))
start_time = perf_counter()
result = fibonacci(n)
end_time = perf_counter()
print(f"斐波那契数列的第{n}项为{result}")
print(f"用时{end_time-start_time}秒")