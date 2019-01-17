import easygraphics.dialog as dlg

values = dlg.get_many_strings("请输入", labels=["身高(米)", "全票票价"])
height = float(values[0])
full_price = float(values[1])
if height <= 1.3:
    price = 0
else:
    if height <= 1.5:
        price = full_price / 2
    else:
        price = full_price

dlg.show_message("最终票价为:" + str(price))
