import easygraphics.dialog as dlg

def calc_sales_price(price):
    if price<0:
        raise ValueError("price should not < 0!")
    sales=0.9*price
    return sales

try:
    price=float(dlg.get_string("请输入价格："))
    sales_price=calc_sales_price(price)
    dlg.show_message(f"打折后价格为{sales_price}")
except ValueError as e:
    print("出现错误",e)
finally:
    print("我总会被执行")