#判断一段文字中是否包含非法关键字
block_words=["傻X","sb","白痴"]
#待检查的文字
text = "你这个大sb！"

#检查是否包含非法关键字
isOk=True
n=len(block_words) #关键字个数
for i in range(n):
    if text.find(block_words[i])>=0:
        isOk=False
        break
        
if isOk:
    print(text)
else:
    print("不要说脏话！")







