import csv
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Sale:
    name : str
    price: Decimal
    quantity: int

def read_csv(filename):
    """
    从csv文件中读取销售记录

    :param filename: csv文件路径
    :return: 销售记录列表
    """
    sales = []
    with open(filename,mode="r",encoding="GBK") as file:
        reader = csv.reader(file)
        row=next(reader)
        for row in reader:
            name = row[0]
            price = Decimal(row[1])
            quantity = int(row[2])
            sale = Sale(name,price,quantity)
            sales.append(sale)
    return sales

def calc_sales_total(sales):
    """
    计算销售总额

    :param sales: 销售记录列表
    :return: 销售总额
    """
    total = 0
    for s in sales:
        amount = s.price * s.quantity
        total += amount
    return total


filename = "4-2-2.销售信息.csv"

sales = read_csv(filename)

print(sales)

total = calc_sales_total(sales)

print(f"销售总额{total}")









