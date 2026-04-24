import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl

mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

# data from United Nations World Population Prospects (Revision 2019)
# https://population.un.org/wpp/, license: CC BY 3.0 IGO
year = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2018]
population_by_continent = {
    '非洲': [.228, .284, .365, .477, .631, .814, 1.044, 1.275],
    '美洲': [.340, .425, .519, .619, .727, .840, .943, 1.006],
    '亚洲': [1.394, 1.686, 2.120, 2.625, 3.202, 3.714, 4.169, 4.560],
    '欧洲': [.220, .253, .276, .295, .310, .303, .294, .293],
    '大洋洲': [.012, .015, .019, .022, .026, .031, .036, .039],
}

plt.stackplot(year, population_by_continent.values(),
             labels=population_by_continent.keys(), alpha=0.8)
plt.legend(loc='upper left', reverse=True)
plt.title('世界人口变化')
plt.xlabel('年份')
plt.ylabel('人口数量(10亿)')
plt.show()