def do_local():
    x = "x local"

def do_global():
    global x
    x = "x global"

x = "test"
do_local()
print("局部赋值后:", x)
do_global()
print("全局赋值后:", x)

