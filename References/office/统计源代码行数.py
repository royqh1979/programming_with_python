from easygraphics import dialog as dlg

import os
from pathlib import Path

package_count = 0
file_count = 0
line_count = 0
def count_source(path:Path, package_name:str):
    global  package_count,file_count,line_count
    package_count+=1
    blank_line_count = 0
    for entry in path.iterdir():
        if not entry.is_file():
            continue
        filename = str(path.absolute()) + os.sep + entry.name
        if filename.endswith(".py") :
            print(filename)
            file_count += 1
            with open(filename,"r",encoding="UTF-8") as file:
                for line in file.readlines():
                    line = line.rstrip()
                    if len(line)==0:
                        blank_line_count+=1
                    else:
                        blank_line_count = 0
                    if blank_line_count>1:
                        continue
                    line_count+=1
    for entry in path.iterdir():
        if not entry.is_dir():
            continue
        if entry.name.startswith("__"):
            continue
        count_source(entry, package_name + "." + entry.name)

dir_path = dlg.get_directory_name("请选择要转换的目录")

path = Path(dir_path)

count_source(path, path.name)

print(f"共有{package_count}个模组，{file_count}个文件，{line_count}行源代码")

