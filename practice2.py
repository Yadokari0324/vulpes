import pandas as pd

name1 = 1
name2 = 2
name3 = 2
name4 = 5
name5 = 3

# 辞書としてデータを準備
data = {
    'name1': [name1],
    'name2': [name2],
    'name3': [name3],
    'name4': [name4],
    'name5': [name5]
}

# 辞書からデータフレームを作成
df = pd.DataFrame(data)

# データフレームの表示
print(df)

