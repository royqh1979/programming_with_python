count = 0
for b1 in range(1,7):
    for b2 in range(1,7):
        if b1 == b2:
            continue
        for b3 in range(1,7):
            if b3 == b1 or b3 == b2:
                continue
            for b4 in range(1,7):
                if b4 == b1 or b4 == b2 or b4 == b3:
                    continue
                for b5 in range(1,7):
                    if b5==b4 or b5==b3 or b5==b2 or b5==b1:
                        continue
                    b6 = 21-b1-b2-b3-b4-b5
                    if b1+b2+b3==b3+b4+b5 and b3+b4+b5==b5+b6+b1:
                        count+=1
                        print(f"    {b3}")
                        print(f"  {b2}   {b4}")
                        print(f"{b1}   {b6}   {b5}")

print(f"共有{count}种填法")