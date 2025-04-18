
def fibonacci(n):
    a=[0]*(n+1)
    a[1]=1
    a[2]=1
    for i in range(3,n+1):
        a[i]=a[i-1]+a[i-2]
    return a[n]


n=int(input("请输入n:"))
result = fibonacci(n)
print(f"斐波那契数列的第{n}项为{result}")