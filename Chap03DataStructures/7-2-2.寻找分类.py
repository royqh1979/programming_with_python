import csv
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Sale:
    name: str
    price: Decimal
    quantity: int


def read_csv(filename):
    """
    从csv文件中读取销售记录并保存到列表中

    :param filename: csv文件名
    :return: 销售记录列表
    """
    sales = []
    with open(filename, mode = "r", encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name = row[0]
            price = Decimal(row[1])
            quantity = int(row[2])
            sale = Sale(name,price,quantity)
            sales.append(sale)
    return sales

def gather_names(sales):
    """
    汇总销售记录中的商品名

    :param sales: 销售记录列表
    :return: 商品名集合
    """
    names = set()
    for sale in sales:
        names.add(sale.name)
    return names

filename = "7-2.sales.csv"
sales = read_csv(filename)

names = gather_names(sales)
print(names)

