# 测试通过多线程同时进行多个numpy计算的性能

import numpy as np
from threading import Thread

from time import perf_counter_ns

def my_function():
    A = np.ones((5000,5000))
    for t in range(100):
        A=A+ones
    return A.sum()

ones = np.ones((5000,5000))
start_time = perf_counter_ns()
for i in range(8):
    my_function()
end_time = perf_counter_ns()
print(f"使用循环: {end_time - start_time}")

threads = [Thread(target=my_function) for i in range(8)]

start_time = perf_counter_ns()
for t in threads:
    t.start()

for t in threads:
    t.join()
end_time = perf_counter_ns()
print(f"使用多线程: {end_time - start_time}")





