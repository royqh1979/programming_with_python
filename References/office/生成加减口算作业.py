#生成一百以内带退位减法 带进位加法

from comtypes.client import CreateObject,Constants
import random


app = CreateObject("Excel.Application")
excel_constants = Constants(app)

template_file = "g:/口算作业模板.xlsx"
out_dir = "g:\\"
out_name = out_dir+"口算"

max_number = 100
ratio_sub = 0.6 #减法题的比例
ratio_carry = 0.8 # 进退位比例
total_page = 40 # 总页数
seciton_per_page = 2 #每页的小节数
row_per_section = 10 #每页的行数
col_per_section = 3 #每页的列数
row_starts=[2, 16]

total_add_with_carry = 0 #带进位加法题目数
total_add_with_no_carry=0 #不带进位加法题目数
total_sub_decomposition = 0 #带退位减法题目数
total_sub_no_decomposition=0 #不带退位减法题目数

workbook = app.Workbooks.open(template_file)
# print(workbook.ActiveSheet.Cells(1,1).Value())

random.seed()
for page in range(total_page):
    for j in range(seciton_per_page):
        row_start = row_starts[j]
        for i in range(row_per_section*col_per_section):
            add_or_sub_ratio=random.random()
            carry_or_not_ratio=random.random()
            row = i%row_per_section+1
            col = i//row_per_section+1
            if add_or_sub_ratio>ratio_sub:
                # 生成加法
                while True:
                    x = random.randint(1,max_number-1)
                    y = random.randint(1,max_number-x)
                    if carry_or_not_ratio<ratio_carry: #需要进位
                        if (x%10)+(y%10) >= 10:
                            total_add_with_carry+=1
                            break
                    else:
                        if (x%10)+(y%10) < 10:
                            total_add_with_no_carry += 1
                            break
                str = f"{x: 3d} + {y: 3d} = "
            else:
                # 生成减法
                while True:
                    x = random.randint(1,max_number)
                    y = random.randint(1,x)
                    if carry_or_not_ratio<ratio_carry: #需要退位
                        if (x % 10) < (y % 10):
                            total_sub_decomposition +=1
                            break
                    else:
                        if (x % 10) >= (y % 10):
                            total_sub_no_decomposition+=1
                            break
                str = f"{x: 3d} - {y: 3d} = "

            workbook.ActiveSheet.Cells(row + row_start, col).Value[()]=str
    out_file = f"{out_name}{page+1:03d}.pdf"
    print(out_file)
    workbook.ActiveSheet.ExportAsFixedFormat(excel_constants.xlTypePDF,out_file,
                                             Quality = excel_constants.xlQualityStandard,
                                             IncludeDocProperties = True,
                                             IgnorePrintAreas=False,
                                             OpenAfterPublish=False)

workbook.Close(SaveChanges=False)
app.Quit()
print(f"加法题目数量：{total_add_with_carry} {total_add_with_no_carry} {total_add_with_carry + total_add_with_no_carry}")
print(f"减法题目数量：{total_sub_decomposition} {total_sub_no_decomposition} {total_sub_decomposition + total_sub_no_decomposition}")