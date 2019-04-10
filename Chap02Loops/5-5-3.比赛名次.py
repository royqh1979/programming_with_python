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
                c_a = c_b = c_c = c_d = c_e = 0
                if b == 2:
                    c_a += 1
                if a == 3:
                    c_a += 1
                if b == 2:
                    c_b += 1
                if e == 4:
                    c_b += 1
                if c==1:
                    c_c += 1
                if d==2:
                    c_c += 1
                if c==5:
                    c_d += 1
                if d==3:
                    c_d += 1
                if e==4:
                    c_e += 1
                if a==1:
                    c_e+=1
                if c_a==1 and c_b==1 and c_c==1 and c_d==1 and c_e==1:
                    print(f"a={a}，b={b},c={c},d={d},e={e}")
