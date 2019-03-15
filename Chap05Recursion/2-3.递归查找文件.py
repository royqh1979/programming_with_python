from pathlib import Path
from easygraphics import dialog as dlg

def find_in_dir(path,key):
    results = []
    for entry in path.iterdir(): # 遍历目录中的所有条目
        if entry.is_dir(): # 如果是子目录
            results0=find_in_dir(entry,key) # 递归在子目录中查找
            results.extend(results0) # 将查找结果并入结果集
        if entry.is_file(): #如果是文件
            if entry.name.find(key)!=-1:
                results.append(str(entry.resolve())) # 找到一个，加入结果集
    return results

dir_path = dlg.get_directory_name("请选择文件夹")
s = dlg.get_string("请输入要查找的关键字:")

dir = Path(dir_path)
results = find_in_dir(dir, s)
for file in results:
    print(file)


