'''
Read and parse CSDN password file
Author: Roy
'''
from easygraphics import dialog as dlg

filename = dlg.get_open_file_name("请输入csdn密码文件：")
if filename == "":
    print("未指定文件")
    exit(-1)

class Account:
    def __init__(self,name,password,email):
        self.name = name
        self.password = password
        self.email = email

accounts = []
with open(filename,mode="r",encoding="UTF-8") as file:
    i=0
    file.readline()
    while True:
        try:
            line = file.readline()
            if line == "" :
                break
            row = line.split("#")
            name = row[0].strip()
            password = row[1].strip()
            email = row[2].strip()
            if name.find("roy")!=-1 or email.find("roy")!=-1:
                account = Account(name,password,email)
                accounts.append(account)
            if i<200:
                print(name,password,email)
                i+=1
        except:
            pass


with open("result.csv",mode="w") as file:
    for account in accounts:
        file.write(f"{account.name},{account.password},{account.email}\n")
