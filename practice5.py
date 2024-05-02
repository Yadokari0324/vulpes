import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

data = {
            'id': [100],
            'error': [1],
            'design': [5],
            'speed': [4],
            'release': [1],
        }

df2 = pd.DataFrame(data)
df2 = df2.set_index('id')
print(df2)
df1 = pd.read_csv("book1.csv", index_col=0)
print(df1)

cos_list = []
for user_id in df1.index:
    cos_list.append(cosine_similarity([df2.loc[100, :]], [df1.loc[user_id, :]]))
df3 = pd.DataFrame([cos_list])
df4 = df3.T
df4.index = df4.index + 1
print(df4)


# DataFrameを水平に連結する
result = pd.concat([df1, df4], axis=1)
result['Index_Column'] = result.index
print(result)