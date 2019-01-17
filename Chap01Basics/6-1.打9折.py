import easygraphics.dialog as dlg


def cals_sales_price(price):
    sales = 0.9 * price
    return sales


price = int(dlg.get_string("请输入原始价格:"))
sales_price = cals_sales_price(price)
dlg.show_message(f"打折后价格为{sales_price}")
