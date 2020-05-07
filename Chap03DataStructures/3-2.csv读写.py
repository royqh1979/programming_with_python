import easygraphics.dialog as dlg
from decimal import Decimal
import csv
from dataclasses import dataclass

@dataclass()
class Sale:
    name: str
    price: Decimal
    quantity: int

# 读取文件
filename = dlg.get_open_file_name("选择要打开的文件", dlg.FileFilter.CSVFiles)
if filename == '':
    print("未选择文件")
    exit(-1)

sales = []
with open(filename,mode="r",encoding="GBK") as file: # with在代码段结束时会自动执行file.close()
    # with会在本段代码结束后自动执行file.close()
    reader = csv.reader(file)
    next(reader) # 跳过csv第一行 (标题行)
    for row in reader:
        name = row[0]
        price = Decimal(row[1])
        quantity = int(row[2])
        sale = Sale(name, price, quantity)
        sales.append(sale)

# 显示读入的结果，以便检查
print("名称\t单价\t数量")
for i in range(len(sales)):
    sale = sales[i]
    print(sale)

# 写入文件
filename = dlg.get_save_file_name("要保存到哪个文件",dlg.FileFilter.CSVFiles)
if filename == '':
    print("未选择文件")
    exit(-1)

with open(filename,mode="w",encoding="GBK") as file:
    file.write(f"商品名称,单价,数量\n")
    for i in range(len(sales)):
        sale = sales[i]
        file.write(f"{sale.name},{sale.price},{sale.quantity}\n")














