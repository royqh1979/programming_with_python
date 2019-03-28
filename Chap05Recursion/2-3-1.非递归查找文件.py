from pathlib import Path
from easygraphics import dialog as dlg
from collections import deque

def find_in_dir(path,key):
    results = []
    queue = deque()
    queue.append(path) #加入队列尾
    while len(queue)>0: #只要队列非空，就继续
        dir = queue.popleft() #从队列头部取出一个目录（并从队列中删除）
        for entry in dir.iterdir(): # 遍历目录中的所有条目
            if entry.is_dir(): # 如果是子目录
                queue.append(entry) # 将子目录加入队列
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


