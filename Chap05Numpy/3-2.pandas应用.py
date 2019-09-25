import numpy as np
import pandas as pd
from easygraphics import dialog as dlg


filename = dlg.get_open_file_name("请选择要打开的csv文件",dlg.FileFilter.CSVFiles)
if filename =="":
    print("未选择文件")
    exit(-1)
with open(filename,mode="r",encoding="GBK") as file:
    df=pd.read_csv(file)
df["销售额"]=df["单价"]*df["数量"]
index=df["销售额"]>100 #生成筛选bool数组
new_df=df[index] #使用bool数组筛选行
new_df.to_csv("result.csv",index=False)
