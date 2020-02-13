#生成一百以内带退位减法 带进位加法

import win32com.client
import random


app = win32com.client.gencache.EnsureDispatch('Excel.Application')
excel_constants = win32com.client.constants

template_file = "g:/竖式作业模板.xlsx"
out_dir = "g:\\"
out_name = out_dir+"竖式"

max_number = 100
ratio_sub = 0.5
total_page = 30 # 总页数
seciton_per_page = 1 #每页的小节数
row_per_section = 8 #每页的行数
col_per_section = 3 #每页的列数
row_starts=[0]

workbook = app.Workbooks.Open(template_file)
# print(workbook.ActiveSheet.Cells(1,1).Value())

random.seed()
for page in range(total_page):
    for j in range(seciton_per_page):
        row_start = row_starts[j]
        for i in range(row_per_section*col_per_section):
            row = (i%row_per_section)*4+1
            col = i//row_per_section+1
            type_ratio=random.random()
            if type_ratio<ratio_sub:
                # 第一项是减法
                while True:
                    x = random.randint(20, max_number)
                    y = random.randint(10, x)
                    # print(x,y,type_ratio)
                    if x-y>10 and y>10:
                        break
                op1_str = f"{x:>2d} - {y:>2d}"
                res1 = x-y
            else:
                # 第一项是加法
                while True:
                    x = random.randint(10, max_number-10)
                    y = random.randint(10, max_number-x)
                    # print(x,y,type_ratio)
                    if 10<x+y<100:
                        break
                op1_str = f"{x:>2d} + {y:>2d}"
                res1=x+y
            if res1<=11:
                type_ratio=1
            elif res1>=89:
                type_ratio=0
            else:
                type_ratio = random.random()
            x = res1
            if type_ratio < ratio_sub:
                # 第一项是减法
                while True:
                    y = random.randint(10, x)
                    # print(x,y,type_ratio)
                    if x-y>0 and y>10:
                        break
                str = f"{op1_str} - {y:>2d}="
            else:
                # 第一项是加法
                while True:
                    y = random.randint(10, max_number-x)
                    # print(x,y,type_ratio)
                    if x+y<100:
                        break
                str = f"{op1_str} + {y:>2d}="
            workbook.ActiveSheet.Cells(row + row_start, col).Value=str
    out_file = f"{out_name}{page+1:03d}.pdf"
    print(out_file)
    workbook.ActiveSheet.ExportAsFixedFormat(excel_constants.xlTypePDF,out_file,
                                             Quality = excel_constants.xlQualityStandard,
                                             IncludeDocProperties = True,
                                             IgnorePrintAreas=False,
                                             OpenAfterPublish=False)

workbook.Close(SaveChanges=False)
app.Quit()

