import easygraphics.dialog as dlg


def calc_sales_price(price):
    """
    计算9折后的价格

    :param price: 折前价格
    :return:  折后价格
    """
    if price < 0:
        raise ValueError("price should not < 0!")
    sales = 0.9 * price
    return sales


price = 100
sales_price = calc_sales_price(price)
dlg.show_message(f"打折后价格为{sales_price}")
