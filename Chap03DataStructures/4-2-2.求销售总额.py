import csv
from decimal import Decimal
import easygraphics.dialog as dlg

class Sale:
    def __init__(self,name,price,quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

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


filename = dlg.get_open_file_name("请选择csv文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件！")
    exit(-1)

sales = read_csv(filename)

dlg.show_objects(sales)

total = calc_sales_total(sales)

dlg.show_message(f"销售总额{total}")









