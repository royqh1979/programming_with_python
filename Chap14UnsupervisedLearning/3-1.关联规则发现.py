import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# ==================== 1. 构造模拟购物篮数据 ====================
# 每一行是一个"事务"（一位顾客的购物小票），包含购买的商品
dataset = [
    ['牛奶', '面包', '尿布'],
    ['牛奶', '面包', '尿布', '啤酒'],
    ['牛奶', '尿布', '鸡蛋'],
    ['面包', '尿布', '啤酒'],
    ['牛奶', '面包', '尿布', '鸡蛋'],
    ['牛奶', '面包', '啤酒'],
    ['面包', '鸡蛋'],
    ['牛奶', '尿布', '啤酒', '鸡蛋'],
    ['面包', '尿布', '鸡蛋'],
    ['牛奶', '面包', '尿布'],
    ['牛奶', '面包'],
    ['尿布', '啤酒'],
    ['牛奶', '尿布', '鸡蛋'],
    ['面包', '尿布'],
    ['牛奶', '面包', '尿布', '啤酒', '鸡蛋'],
    ['牛奶', '面包', '尿布'],
    ['面包', '啤酒'],
    ['牛奶', '尿布'],
    ['牛奶', '面包', '鸡蛋'],
    ['尿布', '鸡蛋']
]

# ==================== 2. 数据预处理：转换为 one-hot 编码 ====================
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)

print("=== One-Hot 编码后的交易矩阵（前5行） ===")
print(df.head())

# ==================== 3. 挖掘频繁项集 ====================
# min_support=0.2 表示项集至少在 20% 的事务中出现
frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

print("\n=== 频繁项集（支持度 ≥ 0.2） ===")
print(frequent_itemsets.sort_values('support', ascending=False))

# ==================== 4. 生成关联规则 ====================
# 以置信度 ≥ 0.6 为阈值提取规则，并计算提升度
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)

# 筛选有意义的规则：提升度 > 1（正相关），并按提升度降序排列
meaningful_rules = rules[rules['lift'] > 1].sort_values('lift', ascending=False)

print("\n=== 强关联规则（置信度 ≥ 0.6 且 提升度 > 1） ===")
print(meaningful_rules[['antecedents', 'consequents',
                         'support', 'confidence', 'lift']].round(3))