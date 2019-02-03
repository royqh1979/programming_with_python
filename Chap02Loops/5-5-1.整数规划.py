max_profit = 0
max_x1,max_x2,max_x3 = 0,0,0

for x1 in range(0,401):
    for x2 in range(0,201):
        if 1.5 * x1 + 3 * x2 > 600:
            break
        if 280 * x1 + 250 * x2 > 60000:
            break
        for x3 in range(0,121):
            if 1.5*x1+3*x2+5*x3>600:
                break
            if 280*x1+250*x2+400*x3>60000:
                break
            profit = 2*x1+3*x2+4*x3
            if profit > max_profit:
                max_profit = profit
                max_x1,max_x2,max_x3 = x1,x2,x3

print(f"小型车{max_x1}辆，中型车{max_x2}辆，大型车{max_x3}辆时有最大利润{max_profit}")