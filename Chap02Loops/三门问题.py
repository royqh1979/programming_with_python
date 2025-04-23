
# 模拟实验次数
num_trials = 100000

# 不换门获胜次数
win_without_switching = 0

# 换门获胜次数
win_with_switching = 0

for i in range(num_trials):
    # 三扇门的编号
    doors = [1, 2, 3]

    # 奖品所在的门的编号
    prize_door = random.randint(1, 3)

    # 参赛者选择的门的编号
    chosen_door = random.randint(1, 3)

    # 未选中且无奖励的门
    non_chosen_non_prize_doors = []
    for door in doors:
        if door != chosen_door and door != prize_door:
            non_chosen_non_prize_doors.append(door)

    # 主持人打开的门的编号
    revealed_door = random.choice(non_chosen_non_prize_doors)

    # 不换门策略
    if chosen_door == prize_door:
        win_without_switching += 1

    # 换门策略
    new_door = None
    for door in doors:
        if door != chosen_door and door != revealed_door:
            new_door = door
            break
    if new_door == prize_door:
        win_with_switching += 1

# 计算获胜概率
win_prob_without_switching = win_without_switching / num_trials
win_prob_with_switching = win_with_switching / num_trials

print("不换门获胜概率：", win_prob_without_switching)
print("换门获胜概率：", win_prob_with_switching)
