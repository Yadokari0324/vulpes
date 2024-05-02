import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

df1 = pd.read_csv("book1.csv", index_col=0)
df2 = pd.read_csv("book2.csv", index_col=0)

print(df1)
print(df2)

cos_list = []
for user_id in df1.index:
    cos_list.append(cosine_similarity([df2.loc[1, :]], [df1.loc[user_id, :]]))
print(cos_list)
df3 = pd.DataFrame([cos_list])
df4 = df3.T
df4.index = df4.index + 1
print(df4)


# DataFrameを水平に連結する
result = pd.concat([df1, df4], axis=1)
 
print(result)

# カラム0のリストから数値を取り出す
# df4['0'] = df4['0'].apply(lambda x: x[0])

# カラム0で降順にソート
df_sorted = result.sort_values(0, ascending=False)

# 結果の表示
print(df_sorted)