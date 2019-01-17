import easygraphics.dialog as dlg

is_girl=dlg.get_yes_or_no("你是女生吗？")
if is_girl:
    dlg.show_message("免费送你个鸡腿~~")

dlg.show_message("继续打饭")
