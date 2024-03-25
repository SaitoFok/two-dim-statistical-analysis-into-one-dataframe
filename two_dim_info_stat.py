# 基于一个表，统计两个维度的数据，并且统计各维度的占比，最后融合为一个表
A = "" # 列名，需要修改
B = "" # 列名，需要修改
input_path = "" # 输入文件路径，需要修改
output_path = "" # 输出文件路径，需要修改

import pandas as pd
df = pd.read_excel(input_path)
df_suxing_gouci = df.groupby([A, B])[B].count().unstack().fillna(0) # 
df_suxing_gouci["总计"] = df_suxing_gouci.sum(axis=1)
df_suxing_gouci["占比"] = df_suxing_gouci["总计"] / df_suxing_gouci["总计"].sum()
df_suxing_gouci["占比"] = df_suxing_gouci["占比"].apply(lambda x: format(x, ".2%"))
# 转置DataFrame
df_suxing_gouci = df_suxing_gouci.T

# 获取除"总计"和"占比"行以外的所有行
rows = [row for row in df_suxing_gouci.index if row not in ['总计', '占比']]
df_temp = df_suxing_gouci.loc[rows]

# 计算素性维度的总计
df_temp['总计'] = df_temp.sum(axis=1)

# 计算素性维度的占比 
total_sum = df_temp['总计'].sum()
df_temp['占比'] = df_temp['总计'] / total_sum
df_temp['占比'] = df_temp['占比'].apply(lambda x: format(x, '.2%'))

# 将"总计"和"占比"两行合并回原DataFrame
df_suxing_gouci = df_suxing_gouci.merge(df_temp[['总计', '占比']], how='left', left_index=True, right_index=True)
# 转置回来
df_suxing_gouci = df_suxing_gouci.T
df_suxing_gouci.to_excel(output_path, index=True)

df_suxing_gouci