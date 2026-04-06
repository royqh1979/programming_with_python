import numpy as np
# 价格序列
prices = np.array([100, 110, 99, 108.9, 95])

daily_log_returns = np.log(prices[1:] / prices[:-1])
daily_returns = (prices[1:]-prices[:-1])/prices[:-1]
print(f"对数收益率:{daily_log_returns.round(4)}")
print(f"简单收益率:{daily_returns.round(4)}")
annual_log_return = np.mean(daily_log_returns) * 252
annual_return = np.mean(daily_returns) * 252
print(f"年化对数收益: {annual_log_return:.4f}")
print(f"年化简单收益: {annual_return:.4f}")
