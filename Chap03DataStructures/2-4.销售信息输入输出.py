from decimal import Decimal

class Sale:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

sales = []
while True:
    name = input("请输入商品名称:")
    if name == "":
        break
    price = Decimal(input("请输入商品价格:"))
    quantity = int(input("请输入购买数量:"))
    sale = Sale(name, price, quantity)
    sales.append(sale)

print("名称\t单价\t数量")
for i in range(len(sales)):
    sale = sales[i]
    print(f"{sale.name}\t{sale.price}\t{sale.quantity}")

