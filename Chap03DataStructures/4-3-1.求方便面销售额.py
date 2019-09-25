import csv
from decimal import Decimal
import easygraphics.dialog as dlg
from dataclasses import dataclass

@dataclass()
class Sale:
    name: int
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

def calc_sub_total(sales, goods_name):
    """
    统计指定商品的销售额
    :param sales: 销售记录列表
    :param goods_name: 要统计的商品名
    :return: 指定商品的销售额
    """
    total = 0
    for s in sales:
        if s.name == goods_name:
            amount = s.price * s.quantity
            total += amount
    return total


filename = dlg.get_open_file_name("请选择csv文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件！")
    exit(-1)

sales = read_csv(filename)

dlg.show_objects(sales)

sub_total = calc_sub_total(sales, "方便面")

dlg.show_message(f"方便面的销售额为{sub_total}元")
