import random

random.seed()
n=10000
bike_a=1000
bike_b=1000
a_to_b_rate = 0.3
b_to_a_rate = 0.4
rented_a = 0
rented_b = 0
missed_a = 0
missed_b = 0
total_a = 0
total_b = 0
for i in range(n):
    r=random.random()
    if r < a_to_b_rate:
        if bike_a > 0:
            rented_a += 1
            bike_a -= 1
            bike_b += 1
        else:
            missed_a += 1
        total_a += 1
    r = random.random()
    if r < b_to_a_rate:
        if bike_b > 0:
            rented_b += 1
            bike_b -= 1
            bike_a += 1
        else:
            missed_b += 1
        total_b += 1

print(f"A: total {total_a} rented {rented_a} missed {missed_a} miss rate: {round(missed_a*100/total_a,2)}% left {bike_a}")
print(f"B: total {total_b} rented {rented_b} missed {missed_b} miss rate: {round(missed_b*100/total_b,2)}% left {bike_b}")


