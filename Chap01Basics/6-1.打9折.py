def cals_sales_price(price):
    sales = 0.9 * price
    return sales


price = int(input("请输入原始价格:"))
sales_price = cals_sales_price(price)
print(f"打折后价格为{sales_price}")
