import pandas as pd

df = pd.read_csv('regression_pls.csv', index_col=0)
aa = df["x1"].head()
for i in aa:
    print(i)