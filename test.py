import inspect

def test(*args,sep=' '):
    fr = inspect.currentframe().f_back
    print(dir(fr))
    datas=[]
    for a in args:
        print(a)
    for var_name, value in fr.f_locals.items():
        print(var_name,value)

def test2():
    x=1
    y=2
    z=3
    test(x,y,z)

test2()
