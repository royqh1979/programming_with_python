import easygraphics.dialog as dlg
from decimal import Decimal

class Sale:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

# 读取文件
filename = dlg.get_open_file_name("选择要打开的文件", dlg.FileFilter.TxtFiles)
if filename == '':
    print("未选择文件")
    exit(-1)

sales = []
file=open(filename,mode="r",encoding="UTF-8")
while True:
    name = file.readline().strip()
    if name == "":
        break
    price = Decimal(file.readline().strip())
    quantity = int(file.readline().strip())
    sale = Sale(name, price, quantity)
    sales.append(sale)
file.close()

# 显示读入的结果，以便检查
print("名称\t单价\t数量")
for i in range(len(sales)):
    sale = sales[i]
    print(f"{sale.name}\t{sale.price}\t{sale.quantity}")

# 写入文件
filename = dlg.get_save_file_name("要保存到哪个文件",dlg.FileFilter.TxtFiles)
if filename == '':
    print("未选择文件")
    exit(-1)


file=open(filename,mode="w",encoding="UTF-8")
for i in range(len(sales)):
    sale = sales[i]
    file.write(f"{sale.name}\t{sale.price}\t{sale.quantity}\n")
file.close()














