height = float(input("请输入身高:"))
full_price = float(input("请输入票价:"))
if height <= 1.3:
    price = 0
else:
    if height <= 1.5:
        price = full_price / 2
    else:
        price = full_price

print("最终票价为:" + str(price))
