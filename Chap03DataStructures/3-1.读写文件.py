import easygraphics.dialog as dlg
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Sale:
    name: str
    price: Decimal
    quantity: int

# 读取文件
filename = dlg.get_open_file_name("选择要打开的文件", dlg.FileFilter.TxtFiles)
if filename == '':
    print("未选择文件")
    exit(-1)

sales = []
file=open(filename,mode="r",encoding="GBK")
# 需要判断是否成功打开（这里省了）
while True:
    name = file.readline() # 读入一行
    print(f"---{name}---")
    name = name.strip() # 去掉读入的回车
    print(f"---**{name}**---")
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


file=open(filename,mode="w",encoding="GBK")
for i in range(len(sales)):
    sale = sales[i]
    file.write(f"{sale.name}\t{sale.price}\t{sale.quantity}\n")
file.close()














