import easygraphics.dialog as dlg

def calc_discount(total):
    """
    计算折扣数和折后金额

    :param total: 购物金额
    :return: 折扣数,折后金额
    """
    if total < 0:
        raise ValueError('total should not < 0!')
    if total >= 500:
        discount_rate=0.9
    elif total >= 200:
        discount_rate=0.95
    else:
        discount_rate = 1
    amount = total * discount_rate
    return discount_rate,amount

total = float(dlg.get_string("请输入总金额"))
dis_rate, amount = calc_discount(total)
dlg.show_message(f"折扣率为{dis_rate},折后金额为{amount}")

