import random

random.seed()
n=10000
prob_a,prob_b = 0.3,0.5
num_a,num_b = 100,100
customer_a,customer_b = 0,0
no_bike_count_a,no_bike_count_b=0,0
for i in range(n):
    want_a = random.uniform(0,1) <= prob_a
    want_b = random.uniform(0,1) <= prob_b
    if want_a:
        customer_a += 1
        if num_a > 0:
            num_a -= 1
            num_b += 1
        else:
            no_bike_count_a += 1
    if want_b:
        customer_b += 1
        if num_b > 0:
            num_b -= 1
            num_a += 1
        else:
            no_bike_count_b += 1

ratio_a = no_bike_count_a / customer_a * 100
ratio_b = no_bike_count_b / customer_b * 100
print(f"A地想租车人数{customer_a},未租到人数{no_bike_count_a}, 未租到比例{ratio_a:0.2f}%")
print(f"B地想租车人数{customer_b},未租到人数{no_bike_count_b}, 未租到比例{ratio_b:0.2f}%")


