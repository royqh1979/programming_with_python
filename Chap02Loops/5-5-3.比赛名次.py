for a in range(1,6):
    for b in range(1,6):
        if b == a :
            continue
        for c in range(1,6):
            if c == b or c == a:
                continue
            for d in range(1,6):
                if d==c or d==b or d==a:
                    continue
                e=15-a-b-c-d
                if b==2 and a==3:
                    continue
                if b!=2 and a!=3:
                    continue
                if b==2 and e==4:
                    continue
                if b!=2 and e!=4:
                    continue
                if c==1 and d==2:
                    continue
                if c!=1 and d!=2:
                    continue
                if c==5 and d==3:
                    continue
                if c!=5 and d!=3:
                    continue
                if e==4 and a==1:
                    continue
                if e!=4 and a!=1:
                    continue
                print(f"a={a}，b={b},c={c},d={d},e={e}")
