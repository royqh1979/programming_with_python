total = 0   #已喝掉的啤酒总数量
beer=5      #现有的还没喝的啤酒数量
bottle = 0  #空瓶数量
lid = 0     #空瓶盖数量
while beer>0: #还有酒可以喝
    # 喝酒
    total = total + beer
    lid = lid + beer
    bottle = bottle + beer
    beer = 0
    # 换酒
    beer = beer + lid //4 + bottle //2
    lid = lid % 4
    bottle = bottle % 2

print(f"总共喝了{total}瓶，剩瓶盖{lid}个，剩酒瓶{bottle}个")
