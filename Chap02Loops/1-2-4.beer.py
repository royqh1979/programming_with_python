beer=0
total = 5
bottle = 5
lid = 5
while lid >= 4 or bottle >=2:
    print(f"换酒前：上轮剩酒{beer}瓶，上轮剩瓶盖换酒{lid//4}瓶，上轮剩瓶子换酒{bottle//2}瓶")
    beer = beer + lid //4 + bottle //2
    lid = lid % 4
    bottle = bottle % 2
    print(f"换酒后：有酒{beer}瓶，剩瓶盖{lid}个，剩酒瓶{bottle}瓶")
    total = total + beer
    lid = lid + beer
    bottle = bottle + beer
    beer = 0
    print(f"喝酒后：总共已喝{total}瓶，剩瓶盖{lid}个，剩酒瓶{bottle}个")
    print("------------------------")
print(f"总共喝了{total}瓶，剩瓶盖{lid}个，剩酒瓶{bottle}个")
