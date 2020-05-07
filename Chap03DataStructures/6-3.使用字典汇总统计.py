import csv
from easygraphics import dialog as dlg
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

def calc_good_totals(sales):
    """
    计算各商品的销售额

    :param sales: 销售记录列表
    :return: 商品销售额字典
    """
    sale_totals = {}
    for sale in sales:
        # 如果字典中还未存在以该记录中的商品名称为关键字的信息，则增加之
        if sale.name not in sale_totals:
            sale_totals[sale.name] = 0
        # 累加对应商品的销售额
        sale_totals[sale.name] += sale.price * sale.quantity
    return sale_totals

filename = dlg.get_open_file_name("请选择csv文件：",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)
sales = read_csv(filename)
totals = calc_good_totals(sales)

for name in totals:
    print(f"商品 {name} 销售了 {totals[name]}元")

