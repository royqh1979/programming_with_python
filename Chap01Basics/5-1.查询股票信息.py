# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 15:25:21 2018

@author: Roy
"""
from urllib import request

#要抓取的股票代码
code="sh601006"
#抓取网页(json格式)
response = request.urlopen('http://hq.sinajs.cn/list='+code)
raw_data=response.read().decode('gbk')

#提取""括起的内容(两个""之间的内容)
quote1=raw_data.find('"')
quote2=raw_data.find('"', quote1 + 1)
raw_data= raw_data[quote1 + 1:quote2]
#按逗号分割成多个数据项
datas=raw_data.split(',')

result="股票{0}目前的价格是{1},最高价{2},最低价{3}".format(datas[0],datas[3],datas[4],datas[5])
#显示查询结果
print(result, "股票信息")

"""
https://www.cnblogs.com/phpxuetang/p/4519446.html
以大秦铁路（股票代码：601006）为例，如果要获取它的最新行情，只需访问新浪的股票数据
接口：
http://hq.sinajs.cn/list=sh601006
这个url会返回一串文本，例如：
var hq_str_sh601006="大秦铁路, 27.55, 27.25, 26.91, 27.55, 26.20, 26.91, 26.92, 
22114263, 589824680, 4695, 26.91, 57590, 26.90, 14700, 26.89, 14300,
26.88, 15100, 26.87, 3100, 26.92, 8900, 26.93, 14230, 26.94, 25150, 26.95, 15220, 26.96, 2008-01-11, 15:05:32";
这个字符串由许多数据拼接在一起，不同含义的数据用逗号隔开了，按照程序员的思路，顺序号从0开始。
0：”大秦铁路”，股票名字；
1：”27.55″，今日开盘价；
2：”27.25″，昨日收盘价；
3：”26.91″，当前价格；
4：”27.55″，今日最高价；
5：”26.20″，今日最低价；
6：”26.91″，竞买价，即“买一”报价；
7：”26.92″，竞卖价，即“卖一”报价；
8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
10：”4695″，“买一”申请4695股，即47手；
11：”26.91″，“买一”报价；
12：”57590″，“买二”
13：”26.90″，“买二”
14：”14700″，“买三”
15：”26.89″，“买三”
16：”14300″，“买四”
17：”26.88″，“买四”
18：”15100″，“买五”
19：”26.87″，“买五”
20：”3100″，“卖一”申报3100股，即31手；
21：”26.92″，“卖一”报价
(22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
30：”2008-01-11″，日期；
31：”15:05:32″，时间；
一个简单的JavaScript应用例子:
<script type="text/javascript" src="http://hq.sinajs.cn/list=sh601006" charset="gb2312"></script>
<script type="text/javascript">
     var elements=hq_str_sh601006.split(",");
    document.write("current price:"+elements[3]);
</script>
这段代码输出大秦铁路（股票代码：601006）的当前股价
current price:14.20
如果你要同时查询多个股票，那么在URL最后加上一个逗号，再加上股票代码就可以了；比如你要一次查询大秦铁路（601006）和大同煤业（601001）的行情，就这样使用URL：
http://hq.sinajs.cn/list=sh601003,sh601001
查询大盘指数，比如查询上证综合指数（000001）：
http://hq.sinajs.cn/list=s_sh000001
服务器返回的数据为：
var hq_str_s_sh000001="上证指数,3094.668,-128.073,-3.97,436653,5458126";
数据含义分别为：指数名称，当前点数，当前价格，涨跌率，成交量（手），成交额（万元）；
查询深圳成指数：
http://hq.sinajs.cn/list=s_sz399001
对于股票的K线图，日线图等的获取可以通过请求http://image.sinajs.cn/…./…/*.gif此URL获取，其中*代表股票代码，详见如下：
查看日K线图：
http://image.sinajs.cn/newchart/daily/n/sh601006.gif

分时线的查询：
http://image.sinajs.cn/newchart/min/n/sh000001.gif

日K线查询：
http://image.sinajs.cn/newchart/daily/n/sh000001.gif

周K线查询：
http://image.sinajs.cn/newchart/weekly/n/sh000001.gif

月K线查询：
http://image.sinajs.cn/newchart/monthly/n/sh000001.gif
"""