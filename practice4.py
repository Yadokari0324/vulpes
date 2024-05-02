import pandas as pd

name1 = 1
name2 = 2
name3 = 3

data = {
    'column1': [name1],
    'column2': [name2],
    'column3': [name3],
}

df = pd.DataFrame(data, index=[100])

print(df)