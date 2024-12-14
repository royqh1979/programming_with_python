import turtle as t

def polygon(n,size):
    for i in range(n):
        t.fd(size)
        t.lt(180-(n-2)*180/n)

n=int(t.numinput("多边形边数","n=",5))
size=int(t.numinput("边长","size=",100))
polygon(n,size)

t.mainloop()