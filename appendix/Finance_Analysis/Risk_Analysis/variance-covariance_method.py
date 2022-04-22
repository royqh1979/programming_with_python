import numpy as np
import pandas as pd
import scipy.stats as st

def VaR_VarCov(market_values, weights, earning_rates, holding_period, confidence_level):
    '''
    运用方差-协方差方法计算投资组合的风险价值
    :param market_values: 投资组合中各资产的当前市值
    :param weights: 投资组合中各资产的权重
    :param earning_rates: 由各资产的日收益率组成的矩阵或数据框
    :param holding_period: 投资组合的持有期（天数）
    :param confidence_level: 置信水平
    :return:
    '''
    earning_rates_mean =earning_rates.mean()    #投资组合中每个资产的平均日收益率
    Rp=np.sum(weights * earning_rates_mean)     #投资组合的平均日收益率
    earning_rates_cov = earning_rates.cov()     #每个资产之间的协方差矩阵
    Vp=np.sqrt(np.dot(weights, np.dot(earning_rates_cov,weights.T))) #计算投资组合收益率的波动率
    z=st.norm.ppf(q=1-confidence_level)
    z=np.abs(z)
    return np.sqrt(holding_period)*market_values*(z*Vp-Rp)